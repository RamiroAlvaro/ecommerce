from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='product_list'),
    url(r'^(?P<slug>[\w_-]+)/$', views.CategoryListView.as_view(), name='category'),
    url(r'^produto/(?P<slug>[\w_-]+)/$', views.product, name='product'),
]