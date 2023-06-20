from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student, name='student'),
    path('student/login/', views.login, name='login'),
    path('student/details/', views.details, name='details'),
    path('student/sign_up/', views.sign_up, name='sign-up'),
    path('student/reset_password/', views.reset_password, name='reset-password'),
]