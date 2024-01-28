
from django.test import TestCase

from .serializers import StudentSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
import io
from rest_framework.parsers import JSONParser

class UserSerializerTest(TestCase):
    def test_valid_password(self):
        password = '123HIi345'
        self.assertEqual(UserSerializer().validate_password(password), password)
        self.assertEqual('sdeisQ1234@', UserSerializer().validate_password('sdeisQ1234@'))

    def test_password_too_short(self):
        password = '123'
        with self.assertRaises(ValidationError) as cm:
            UserSerializer().validate_password(password)

    def test_password_no_digit(self):
        password = 'abdcdgsQsdf'
        with self.assertRaises(ValidationError) as cm:
            UserSerializer().validate_password(password)

    def test_password_no_lower_case(self):
        password = 'AAAAAAQ134'
        with self.assertRaises(ValidationError) as cm:
            UserSerializer().validate_password(password)

    def test_password_no_upper_case(self):
        password = 'abcdeds134'
        with self.assertRaises(ValidationError) as cm:
            UserSerializer().validate_password(password)

    def test_create_user_failed_failed(self):
        user_json = {'username': 'test', 'password': '123', 'last_name': 'wu', 'first_name': 'david'}

        with self.assertRaises(ValidationError) as cm:
            serializer = UserSerializer(data=user_json)
            self.assertFalse(serializer.is_valid(raise_exception=True))
    
    def test_create_user_success(self):
        user_json = {'username': 'test', 'password': 'sdeisQ1234', 'last_name': 'wu',
                     'first_name': 'david'}

        user_serializer = UserSerializer(data=user_json)
        self.assertTrue(user_serializer.is_valid(raise_exception=True))
        user = user_serializer.create(user_serializer.validated_data)
        user.save()
        saved_user=User.objects.get(username='test')
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.password, 'sdeisQ1234')

    def test_create_student_success(self):
        student_json = {'first_name': 'sandy', 'last_name': 'zhao',
                        'middle_name': 'dfd', 'gender': 'F', 'date_of_birth': '2016-02-01',
                        'chinese_name': ''}
        student_serializer = StudentSerializer(data=student_json)
        self.assertTrue(student_serializer.is_valid(raise_exception=True))
        




    