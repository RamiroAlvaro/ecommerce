from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^carrinho/adicionar/(?P<slug>[\w_-]+)$', views.CreateCartItem.as_view(), name='create_cartitem'),
    url(r'^finalizando/$', views.CheckoutView.as_view(), name='checkout'),
    url(r'^carrinho/$', views.CartItemView.as_view(), name='cart_item'),
    url(r'^meus-pedidos/$', views.OrderListView.as_view(), name='order_list'),
    url(r'^meus-pedidos/(?P<pk>\d+)/$', views.OrderDetailView.as_view(), name='order_detail'),
]