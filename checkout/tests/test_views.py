from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy

from checkout.models import CartItem

from catalog.models import Product


class CreateItemTestCase(TestCase):

    def setUp(self):
        self.product = mommy.make(Product)
        self.client = Client()
        self.url = reverse('checkout:create_cartitem', kwargs={'slug': self.product.slug})

    def tearDown(self):
        self.product.delete()
        CartItem.objects.all().delete()

    def test_add_cart_item_simple(self):
        response = self.client.get(self.url)
        redirect_url = reverse('checkout:cart_item')
        # Dos maneras de testar redireccionamiento
        self.assertRedirects(response, redirect_url)
        self.assertEqual(response.status_code, 302)
        self.assertEquals(CartItem.objects.count(), 1)

    def test_add_cart_item_complex(self):
        self.client.get(self.url)
        self.client.get(self.url)
        cart_item = CartItem.objects.get()
        self.assertEquals(cart_item.quantity, 2)


class CheckoutViewTestCase(TestCase):

    def setUp(self):
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
        self.cart_item = mommy.make(CartItem)
        self.client = Client()
        self.url_checkout = reverse('checkout:checkout')

    def test_checkout_view(self):
        response = self.client.get(self.url_checkout)
        redirect_url = '{}?next={}'.format(reverse(settings.LOGIN_URL), self.url_checkout)
        self.assertRedirects(response, redirect_url)
        self.client.login(username=self.user.username, password='123')
        self.cart_item.cart_key = self.client.session.session_key
        self.cart_item.save()
        response = self.client.get(self.url_checkout)
        self.assertTemplateUsed(response, 'checkout/checkout.html')