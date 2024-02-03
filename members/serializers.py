from rest_framework import serializers
from .models import Member, Student, Course, Registration
from django.contrib.auth.models import User
import re
import pytz
from datetime import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
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
        if datetime.now().year - dob.year < 4:
            raise ValueError('Minimum age requirement is not satisfied!')
        return dob
    
    def validate_gender(self, gender):
        if not gender or gender.upper() not in ('U', 'M', 'F', 'FEMALE', 'MALE'):
            raise ValueError("invalid gender information!")
        return gender
    def to_internal_value(self, data):
        if data.get('chinese_name', None) == '':
            data.pop('chinese_name')
        if data.get('middle_name', None) == '':
            data.pop('middle_name')
        return super().to_internal_value(data)
    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'course_description', 'course_type',
                  'course_status', 'size_limit', 'cost')
    
    def validate_course_type(self, course_type):
        if course_type not in ['L', 'E']:
            raise ValueError("Invalid course type")
        return course_type
    
    def validate_name(self, name):
        if not name:
            raise ValueError("No name is provided for the course")
        
        return name

    def validate_size_limit(self, size_limit):
        if size_limit < 0:
            raise ValueError("Invalid course size limit!")
        return size_limit

    def validate_course_status(self, course_status):
        if course_status not in ['A', 'U']:
            raise ValueError("Invalid course status!")
        return course_status
    
    def validate_cost(self, cost):
        if cost < 0:
            raise ValueError("invalid cost for the new course!")
        return cost

    def create(self, validated_data, username, member):
        course = Course(**validated_data)
        course.creation_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        course.last_update_time = course.creation_date
        course.creater_name = username
        course.last_update_person = member
        return course
    
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ('registration_code', 'school_year_start', 'school_year_end',
                  'registration_date', 'expiration_date')
    
    def create(self, validated_data, student, course):
        registration = Registration(**validated_data)
        registration.registration_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        registration.student = student
        registration.course = course
        return registration
    



