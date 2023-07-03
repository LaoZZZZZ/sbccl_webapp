from django.db import models

# Create your models here.
class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    recovery_email = models.CharField(max_length=255)
    registration_date = models.DateField(null=True)
    password = models.CharField(max_length=255)
    phone_number = models.IntegerField(null=True)
    user_name = models.CharField(max_length=255, null=True)
