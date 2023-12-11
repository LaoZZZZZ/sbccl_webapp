
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from .models import Member
from .serializers import UserSerializer
from django.contrib.auth.models import User

class MemberViewSetTest(APITestCase):
    def test_create_member_succeed(self):
        user_json = {'username': 'test_name', 'password': 'helloworld12H',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        client = APIClient()
        response = client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id.username, 'test_name')
        user = User.objects.get(username='test_name')
        self.assertEqual(user.password, 'helloworld12H')
    
    def test_create_member_conflit_username_fail(self):
        # set up

        exist_user = User.objects.create(
            username='test_name',
            password='helloworld12H'
        )
        exist_user.save()

        user_json = {'username': 'test_name', 'password': 'helloworld12H',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        client = APIClient()
        response = client.post('/rest_api/members/', data=user_json, format='json')
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
        client = APIClient()
        response = client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_create_member_invalid_password_fail(self):
        user_json = {'username': 'different_name', 'password': 'invalid',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        client = APIClient()
        response = client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        print(response)

    # def test_user_login_succeed(self):

    #     exist_user = User.objects.create(
    #         username='test_name',
    #         password='helloworld12H',
    #         email='david@gmail.com'
    #     )
    #     exist_user.save()

    #     client = APIClient()
    #     response = client.put('/rest_api/members/test_name/login/', format='json')
    #     self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)