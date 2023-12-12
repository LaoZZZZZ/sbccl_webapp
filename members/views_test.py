
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from .models import Member
from .serializers import UserSerializer
from .views import MemberViewSet
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate

class MemberViewSetTest(APITestCase):
    def create_user(self, user_name, email):
        exist_user = User.objects.create(
            username=user_name,
            password='helloworld12H',
            email=email
        )
        exist_user.save()
        return exist_user

    def create_member(self, user, sign_up_status='V', verification_code=None):
        member = Member.objects.create(
            user_id=user,
            member_type='P',
            sign_up_status=sign_up_status,
            phone_number=123451335,
            verification_code=verification_code
        )
        member.save()

    def test_create_member_succeed(self):
        user_json = {'username': 'test_name', 'password': 'helloworld12H',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id.username, 'test_name')
        user = User.objects.get(username='test_name')
        self.assertEqual(user.password, 'helloworld12H')
        created_member = Member.objects.get(user_id=user)
        self.assertEqual(created_member.sign_up_status, 'S')
        self.assertEqual(created_member.member_type, 'P')
    
    def test_create_member_conflit_username_fail(self):
        # set up
        exist_user = User.objects.create(
            username='test_name',
            password='helloworld12H'
        )
        exist_user.save()

        user_json = {'username': 'test_name', 'password': 'helloworld12H',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_member_conflit_email_fail(self):
        # set up
        exist_user = User.objects.create(
            username='test_name',
            password='helloworld12H',
            email='david@gmail.com'
        )
        exist_user.save()

        user_json = {'username': 'different_name', 'password': 'helloworld12H',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_member_invalid_password_fail(self):
        user_json = {'username': 'different_name', 'password': 'invalid',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response)

    def test_user_login_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/test_name/login/',format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        response = self.client.put('/rest_api/members/test_name/logout/',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_exist_user_login_failed(self):
        non_exist_user = User.objects.create(
            username='test_name',
            password='helloworld12H',
            email='david@gmail.com'
        )

        self.client.force_authenticate(user=non_exist_user)
        response = self.client.put('/rest_api/members/test_name/login/',format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_non_exist_member_login_failed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/test_name/login/',format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_verify_user_succeed(self):
        verification_code = "12345-abc"
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='S', verification_code=verification_code)

        response = self.client.put('/rest_api/members/test_name/verify-user/',
                                   {"verification_code": verification_code}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        verifed_member = Member.objects.get(user_id=exist_user)
        self.assertEqual(verified_member.sign_up_status, 'V')
        self.assertEqual(verified_member.verification_code, '')

    def test_verify_user_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)
        
        self.client.force_authenticate(user=exist_user)
    def test_add_student(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        self.client.force_authenticate(user=exist_user)
