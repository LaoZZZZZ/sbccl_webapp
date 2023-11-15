from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('details/', views.details, name='details'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_up_confirmation/', views.sign_up_confirmation, name='sign_up'),
    path('reset_password/', views.reset_password, name='reset-password'),
]