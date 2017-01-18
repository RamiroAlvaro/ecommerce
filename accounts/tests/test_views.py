from django.test import Client, TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.conf import settings

from model_mommy import mommy

User = get_user_model()


class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_register_ok(self):
        data = dict(username='Ramiro', password1='teste123', password2='teste123', email='ramiroalvaro.ra@gmail.com')
        response = self.client.post(self.register_url, data)
        index_url = reverse('index')
        self.assertRedirects(response, index_url)
        self.assertEqual(User.objects.count(), 1)

    def test_register_error(self):
        data = dict(username='Ramiro', password1='teste123', password2='teste123')
        response = self.client.post(self.register_url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdateUserTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.update_url = reverse('accounts:update_user')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_user_ok(self):
        data = {'name': 'ramiro', 'email': 'ramiroalvaro.ra@gmail.com'}
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.update_url, data)
        accounts_index_url = reverse('accounts:index')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, accounts_index_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email,'ramiroalvaro.ra@gmail.com')
        self.assertEqual(self.user.name, 'ramiro')

    def test_update_user_error(self):
        data = {}
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.update_url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdatePasswordTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.update_url = reverse('accounts:update_password')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_update_password_ok(self):
        data = {'old_password': '123', 'new_password1': 'teste123', 'new_password2': 'teste123'}
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.update_url, data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('teste123'))



