from django.test import TestCase, Client
from django.core.urlresolvers import reverse


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('index')
        self.response = self.client.get(self.url)

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, 'index.html')