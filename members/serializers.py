from rest_framework import serializers
from .models import Member, Student
from django.contrib.auth.models import User
import re
import pytz
from datetime import datetime

class LoginFormSerializer(serializers.Serializer):
    pass

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.date_joined = datetime.utcnow().replace(tzinfo=pytz.utc)
        return user
    
    def validate_password(self, password):
        """
        Check if the password is valid
        1. Must be at least 8 characters long
        2. Must contain one lower case character
        3. Must contain one upper case character
        4. Must contain a digit from 0-9
        """
        if len(password) < 8:
            raise serializers.ValidationError("The password is too short!")
        if not re.search("[0-9]+", password):
            raise serializers.ValidationError("The password should at least contain one digit")
        if not re.search("[a-z]+", password):
            raise serializers.ValidationError("The password should at least contain lower case")
        if not re.search("[A-Z]+", password):
            raise serializers.ValidationError("The password should at least contain upper case")
        return password

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('user_id', 'phone_number', 'sign_up_status', 'member_type')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name', 'gender',
                  'date_of_birth', 'joined_date', 'chinese_name')

    def create(self, validated_data):
        student = Student(**validated_data)
        student.joined_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        return student

    """
    Raise ValueError if validation failed
    """
    def validate_date_of_birth(self, date_of_birth_str):
        dob = datetime.strptime(str(date_of_birth_str), '%Y-%m-%d')
        if datetime.now().year - dob.year < 5:
            raise ValueError('Minimum age requirement is not satisfied!')
        return dob
    
    def validate_first_name(self, first_name):
        if first_name is None or first_name == '':
            raise ValueError("First name is empty!")
        return first_name
    
    def validate_last_name(self, last_name):
        if last_name is None or last_name == '':
            raise ValueError("Last name is empty!")
        return last_name
    
    def validate_gender(self, gender):
        if not gender or gender.upper() not in ('M', 'F', 'FEMALE', 'MALE'):
            raise ValueError("invalid gender information!")
        return gender



