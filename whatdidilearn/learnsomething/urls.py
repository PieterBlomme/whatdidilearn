from django.conf.urls import url
from django.urls import path
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
    path('<str:user>/', views.user_library, name='user_library'),
    path('', views.home, name='home'), #TODO: make sure URL only works for home page (separate app?)
    url(r'library', views.add_to_lib, name='add to library'),
    path('detail/add/', views.add_paper, name='add paper'),
    path('add/tag', views.add_tag, name='add tag'),
    path('detail/<str:pk_paper>/delete_tag/<str:pk>/', views.delete_tag, name='delete tag'),
    path('add/benchmark', views.add_benchmark, name='add benchmark'),
    path('detail/<str:pk_paper>/delete_benchmark/<str:pk>/', views.delete_benchmark, name='delete benchmark'),
    path('add/comment', views.add_comment, name='add comment'),
    path('detail/<str:pk_paper>/delete_comment/<str:pk>/', views.delete_comment, name='delete comment'),
    path('detail/<str:pk>/', views.ArticleDetailView.as_view(), name='detail'),
]