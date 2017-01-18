from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^registro/$', views.RegisterView.as_view(), name='register'),
    url(r'^alterar-dados/$', views.UpdateUserView.as_view(), name='update_user'),
    url(r'^alterar-senha/$', views.UpdatePasswordView.as_view(), name='update_password'),
]
