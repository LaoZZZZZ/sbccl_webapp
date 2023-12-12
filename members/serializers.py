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
        fields = ('username', 'email', 'first_name', 'last_name', 'date_joined', 'password')

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
        fields = ('parent_id', 'first_name', 'last_name', 'middle_name', 'gender',
                  'date_of_birth', 'joined_date', 'chinese_name')

    def validate_date_of_birth(self):
        pass

