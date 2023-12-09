from django.test import Client
from django.urls import reverse
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from .views import MemberViewSet
from .models import Member

class MemberViewSetTest(APITestCase):
    def test_create_member(self):
        factory = APIRequestFactory()
        client = APIClient()
        data = {'username': 'test_name', 'password': 'helloworld',
                'email': 'luzhao@gmail.com', 'first_name': 'Lu', 'last_name': 'Zhao'}
        # url = reverse(MemberViewSet.as_view(actions={'post': 'create'}))
        # request = factory.put('/rest_api/members/login/', data, format='json')
        client.login(username='luzhao', password='helloworld')
        response = client.put('/rest_api/members/login/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id, 'test_name')