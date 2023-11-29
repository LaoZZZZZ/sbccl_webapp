from django.urls import path
from . import views

urlpatterns = [
    # path('', views.user, name='user'),
    path('login/', views.login, name='login'),
    path('details/', views.details, name='details'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('password_reset_confirmation/', views.password_reset_confirmation, name='password_reset_confirmation'),
    path('sign_up_confirmation/', views.sign_up_confirmation, name='sign_up'),
    path('verify_user/', views.verify_user, name='verify_user'),
]