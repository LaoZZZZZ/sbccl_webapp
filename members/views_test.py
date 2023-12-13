
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from .models import Member, Student
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
        return member

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

        response = self.client.put('/rest_api/members/test_name/verify-user/?verification_code=12345-abc',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        verifed_member = Member.objects.get(user_id=exist_user)
        self.assertEqual(verifed_member.sign_up_status, 'V')
        self.assertIsNone(verifed_member.verification_code)

    def test_verify_user_not_found(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        response = self.client.put('/rest_api/members/test_name/verify-user/?verification_code=12345-abc',
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reset_password_by_code_succeed(self):
        verification_code = "12345-abc"
        new_password = 'HelloWorld1'
        url = '/rest_api/members/test_name/reset-password-by-code/?verification_code={code}&new_password={pw}'.format(code = verification_code, pw=new_password)
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='S', verification_code=verification_code)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        verifed_member = Member.objects.get(user_id=exist_user)
        self.assertIsNone(verifed_member.verification_code)
        updated_user = User.objects.get(username='test_name')
        self.assertEqual(updated_user.password, new_password)
    
    def test_reset_password_by_code_fail(self):
        verification_code = "12345-abc"
        new_password = 'HelloWorld1'
        url = '/rest_api/members/test_name/reset-password-by-code/?verification_code={code}&new_password={pw}'.format(code = verification_code, pw=new_password)
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V', verification_code='')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.get(username='test_name').password, exist_user.password)

    def test_reset_invalid_password_by_code_fail(self):
        verification_code = "12345-abc"
        new_password = 'invalid'
        url = '/rest_api/members/test_name/reset-password-by-code/?verification_code={code}&new_password={pw}'.format(code = verification_code, pw=new_password)
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V', verification_code='')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.get(username='test_name').password, exist_user.password)

    def test_reset_password_via_login_succeed(self):
        new_password = 'HelloWorld1'
        url = '/rest_api/members/test_name/reset-password/?new_password={pw}'.format(pw=new_password)
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V')
        
        self.client.force_authenticate(user=exist_user)
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        verifed_member = Member.objects.get(user_id=exist_user)
        self.assertIsNone(verifed_member.verification_code)
        updated_user = User.objects.get(username='test_name')
        self.assertEqual(updated_user.password, new_password)

    def test_add_student_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/test_name/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Member.objects.get(user_id=exist_user)
        student = Student.objects.get(parent_id=member)
        self.assertEqual(student.last_name, 'chatty')
        self.assertEqual(student.first_name, 'david')
        self.assertIsNotNone(student.joined_date)

        response = self.client.put('/rest_api/members/test_name/add-student/',
                            data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


    def test_add_invalid_student_fail(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        student_json = {
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/test_name/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_student_to_ineligible_member_fail(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)
        member = Member.objects.get(user_id=exist_user)
        member.member_type = 'B'
        member.save()

        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/test_name/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_add_student(self):
    #     exist_user = self.create_user('test_name', 'david@gmail.com')
    #     self.create_member(exist_user)

    #     self.client.force_authenticate(user=exist_user)
