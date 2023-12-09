from rest_framework import serializers
from .models import Member, Student, Course, Payment, Registration
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'password')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('parent_id', 'first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'joined_date', 'chinese_name')

