from rest_framework import serializers
from .models import User, Student

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'joined_date', 'password',
                   'phone_number', 'sign_up_status', 'verification_code')
        
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('parent_id', 'first_name', 'last_name', 'middle_name', 'gender', 'date_of_birth', 'joined_date', 'chinese_name')

