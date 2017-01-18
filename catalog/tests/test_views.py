from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from model_mommy import mommy

from catalog.models import Category, Product


class ProductListTestCase(TestCase):

    def setUp(self):
        self.url = reverse('catalog:product_list')
        self.client = Client()
        self.products = mommy.make(Product, _quantity=10)

    def tearDown(self):
        Product.objects.all().delete()

    def test_status_code_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/product_list.html')

    def test_context(self):
        response = self.client.get(self.url)
        self.assertTrue('product_list' in response.context)
        product_list = response.context['product_list']
        # Paginacion de 6 productos en ProductListView
        self.assertEqual(product_list.count(), 6)
        # Testear numero de paginas para 10 productos con paginacion por 6
        paginator = response.context['paginator']
        self.assertEqual(paginator.num_pages, 2)

    def test_page_not_found(self):
        response = self.client.get('{}?page=5'.format(self.url))
        self.assertEqual(response.status_code, 404)