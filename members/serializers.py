from rest_framework import serializers
from .models import Member, Student, Course, Registration, Coupon, SchoolCalendar, Dropout, Payment 
from django.contrib.auth.models import User
import re
import pytz
from datetime import datetime, date

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
        fields = ('user_id', 'phone_number', 'sign_up_status', 'member_type', 'term_signed_date')

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'middle_name', 'gender',
                  'date_of_birth', 'joined_date', 'chinese_name')
    
    def calculateAge(dob : date):
        days_in_year = 365.2425   
        return int((datetime.today().date() - dob).days / days_in_year)

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
                  'course_status', 'size_limit', 'cost', 'classroom',
                  'course_start_time', 'course_end_time', 'book_cost')
    
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

    def validate_book_cost(self, book_cost):
        if book_cost < 0:
            raise ValueError("invalid book cost for the new course!")
        return book_cost

    def validate_classroom(self, classroom):
        if not classroom:
            raise ValueError("Invalid classroom assignment")
        return classroom

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
        fields = ('id', 'registration_code', 'school_year_start', 'school_year_end',
                  'registration_date', 'expiration_date', 'course', 'student',
                  'on_waiting_list', 'coupons', 'textbook_ordered')
    
    def create(self, validated_data, student, course):
        registration = Registration(**validated_data)
        registration.registration_date = datetime.utcnow().replace(tzinfo=pytz.utc)
        registration.student = student
        registration.course = course
        return registration

class DropoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dropout
        fields = ('id', 'course_name', 'student', 'school_year_start', 'school_year_end',
                  'original_registration_code', 'dropout_date')
    
class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = ('reason', 'type', 'dollar_amount', 'percentage', 'code', 'application_rule',
                  'expiration_date')

    def create(self, validated_data, user : User):
        coupon = Coupon(**validated_data)
        coupon.creation_date = datetime.date.today()
        coupon.creator = user.username
        return coupon
    
    
class SchoolCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolCalendar
        fields = ('event', 'date', 'school_year_start', 'school_year_end', 'day_type')

    def create(self, validated_data):
        school_date = SchoolCalendar(**validated_data)
        school_date.creation_date = datetime.date.today()
        return school_date
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        # registraiton_code is actually the id of the registration.
        fields = ('registration_code', 'pay_date', 'original_amount', 'amount_in_dollar',
                  'payment_method', 'payment_status', 'last_udpate_date')
    