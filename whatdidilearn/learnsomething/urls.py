from django.conf.urls import url
from learnsomething import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView # new

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset_done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'home', views.home, name='home') #TODO: make sure URL only works for home page (separate app?)
]