from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail


class IndexViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'index.html')


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'contact.html')

    def test_form_errors(self):
        data = {'name': '', 'email': '', 'message': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_form_ok(self):
        data = {'name': 'Ramiro Alvaro', 'email': 'ramiroalvaro.ra@gmail.com', 'message': 'Hola mundo !!!'}
        response = self.client.post(self.url, data)
        self.assertTrue(response.context['success'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Contato do Ecommerce')