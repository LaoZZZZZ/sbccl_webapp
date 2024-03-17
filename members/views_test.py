
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from .models import Member, Student, Course, Registration
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
import datetime

class MemberViewSetTest(APITestCase):
    def create_user(self, user_name, email):
        exist_user = User.objects.create(
            username=user_name,
            email=email
        )
        exist_user.set_password('helloworld12H')
        exist_user.save()
        return User.objects.get(username=user_name)

    def create_member(self, user, sign_up_status='V', verification_code=None,
                      member_type='P'):
        member = Member.objects.create(
            user_id=user,
            member_type=member_type,
            sign_up_status=sign_up_status,
            phone_number=123451335,
            verification_code=verification_code
        )
        member.save()
        return member

    def test_create_member_succeed(self):
        user_json = {'username': 'test3@gmail.com', 'email': 'test3@gmail.com',
                      'first_name': 'Sandy', 'last_name': 'Zhao', 'password': 'Helloworld1'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id.username, 'test3@gmail.com')
        user = User.objects.get(username='test3@gmail.com')
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

    def test_create_member_invalid_password_fail(self):
        user_json = {'username': 'different_name', 'password': 'invalid',
                     'email': 'david@gmail.com', 'first_name': 'david', 'last_name': 'Rob'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/login/',format='json')
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
        url = '/rest_api/members/verify-user/?verification_code={code}&email={email}'.format(
            code=verification_code, email='david@gmail.com')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        verifed_member = Member.objects.get(user_id=exist_user)
        self.assertEqual(verifed_member.sign_up_status, 'V')
        self.assertIsNone(verifed_member.verification_code)

    def test_verify_user_not_found(self):
        self.create_user('test_name', 'david@gmail.com')
        url = '/rest_api/members/verify-user/?verification_code={code}&email={email}'.format(
            code='12345-abc', email='david@gmail.com')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_password_reset_code(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='S')

        response = self.client.put('/rest_api/members/create-password-reset-code/?email={email}'.format(email='david@gmail.com'),
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        updated_member = Member.objects.get(user_id=exist_user)
        self.assertEqual(updated_member.verification_code, response['location'])

    def test_reset_password_by_code_succeed(self):
        verification_code = "12345-abc"
        new_password = 'HelloWorld1'
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='S', verification_code=verification_code)
        url = '/rest_api/members/reset-password-by-code/?verification_code={code}&password={password}&email={email}'.format(code=verification_code, password=new_password, email='david@gmail.com')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        verifed_member = Member.objects.get(user_id=exist_user)
        self.assertIsNone(verifed_member.verification_code)
    
    def test_reset_password_by_code_fail(self):
        verification_code = "12345-abc"
        new_password = 'HelloWorld1'
        url = '/rest_api/members/reset-password-by-code/?verification_code={code}&new_password={pw}'.format(code=verification_code, pw=new_password)
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V', verification_code='')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.get(username='test_name').password, exist_user.password)

    def test_reset_invalid_password_by_code_fail(self):
        verification_code = "12345-abc"
        new_password = 'invalid'
        url = '/rest_api/members/reset-password-by-code/?verification_code={code}&new_password={pw}'.format(code = verification_code, pw=new_password)
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V', verification_code='')
        response = self.client.put(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.get(username='test_name').password, exist_user.password)

    def test_reset_password_via_login_succeed(self):
        new_password = 'HelloWorld1'
        url = '/rest_api/members/reset-password/?new_password={pw}'.format(pw=new_password)
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
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Member.objects.get(user_id=exist_user)
        student = Student.objects.get(parent_id=member)
        self.assertEqual(student.last_name, 'chatty')
        self.assertEqual(student.first_name, 'david')
        self.assertIsNotNone(student.joined_date)

        response = self.client.put('/rest_api/members/add-student/',
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
        response = self.client.put('/rest_api/members/add-student/',
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
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_student_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Member.objects.get(user_id=exist_user)
        student = Student.objects.get(parent_id=member)
        self.assertEqual(student.last_name, 'chatty')
        self.assertEqual(student.first_name, 'david')
        self.assertIsNotNone(student.joined_date)

        response = self.client.put('/rest_api/members/remove-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_remove_non_existing_student_no_op(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=exist_user)

        response = self.client.put('/rest_api/members/remove-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_course_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        persited_course = Course.objects.get(name='B1A')
        self.assertEqual(persited_course.cost, 500)
        self.assertEqual(persited_course.course_description,
                         'Morning session for grade 1 class.')
        self.assertEqual(persited_course.course_type, 'L')
        self.assertEqual(persited_course.course_status, 'A')
        self.assertEqual(persited_course.creater_name, 'test_name')
        self.assertEqual(persited_course.size_limit, 20)
        self.assertIsNotNone(persited_course.creation_date)
        self.assertIsNotNone(persited_course.last_update_time)
        self.assertEqual(persited_course.last_update_person, exist_user.username)

        updated_course = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class 2024.',
            'course_type': "L",
            'course_status': 'U',
            'size_limit': 1,
            'cost': 400
        }
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=updated_course, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        persited_course = Course.objects.get(name='B1A')
        self.assertEqual(persited_course.cost, 400)
        self.assertEqual(persited_course.course_description,
                         'Morning session for grade 1 class 2024.')
        self.assertEqual(persited_course.course_type, 'L')
        self.assertEqual(persited_course.course_status, 'U')
        self.assertEqual(persited_course.creater_name, 'test_name')
        self.assertEqual(persited_course.size_limit, 1)
        self.assertIsNotNone(persited_course.creation_date)
        self.assertIsNotNone(persited_course.last_update_time)
        self.assertEqual(persited_course.last_update_person, exist_user.username)

    def test_list_course_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.get('/rest_api/members/list-courses/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['courses']), 1)
        import json
        obtained_course = json.loads(response.data['courses'][0])
        self.assertEqual(obtained_course['name'], 'B1A')
        self.assertTrue('id' in obtained_course)

    def test_add_registration_course_succeed(self):
        # Add class first
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        persisted_course = Course.objects.get(name="B1A")
        # Add student
        parent_account = self.create_user('parent', 'parent@gmail.com')
        self.create_member(parent_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Member.objects.get(user_id=parent_account)
        student = Student.objects.get(parent_id=member)
        self.assertEqual(student.last_name, 'chatty')
        self.assertEqual(student.first_name, 'david')
        self.assertIsNotNone(student.joined_date)
        # Add registration
        payload = {
            'course_id': persisted_course.id,
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registration = Registration.objects.get(student=student)
        self.assertEqual(registration.course.name, "B1A")
        self.assertEqual(registration.student.last_name, student.last_name)
        self.assertEqual(registration.student.first_name, student.first_name)
        self.assertIsNotNone(registration.school_year_start)
        self.assertIsNotNone(registration.school_year_end)
        self.assertEqual(registration.registration_date.day, datetime.datetime.today().day)

        # make sure the student can also be searched 
        updated_course = Course.objects.get(name='B1A')
        updated_course.students.get(first_name=student.first_name)

    def test_add_registration_nonexisting_course_fail(self):
        parent_account = self.create_user('parent', 'parent@gmail.com')
        self.create_member(parent_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=parent_account)
        
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        member = Member.objects.get(user_id=parent_account)
        student = Student.objects.get(parent_id=member)
        # Add registration
        payload = {
            'course_id': '1335',
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            }
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put('/rest_api/members/register-course/',
                            data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_add_registe_nonexisting_student_fail(self):
        board_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(board_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=board_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        persited_course = Course.objects.get(name='B1A')
        parent_account = self.create_user('parent', 'parent@gmail.com')
        self.create_member(parent_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        self.client.force_authenticate(user=parent_account)
        # Add registration
        payload = {
            'course_id': persited_course.id,
            'student': {
                'first_name': "nonexist",
                'last_name': "nonexist",
                'date_of_birth': datetime.datetime.today(),
                'gender': 'M'
            }
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.put('/rest_api/members/register-course/',
                            data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_registration_conflict_student_fail(self):
        # Add class first
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        second_course = {
            'name': "B2A",
            'course_description': 'Morning session for grade 2nd class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=second_course, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add student
        parent_account = self.create_user('parent', 'parent@gmail.com')
        self.create_member(parent_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Member.objects.get(user_id=parent_account)
        student = Student.objects.get(parent_id=member)
        persisted_course = Course.objects.get(name="B1A")
        # Add registration
        payload = {
            'course_id': persisted_course.id,
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        second_course = Course.objects.get(name='B2A')
        new_registration = {
            'course_id': second_course.id,
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=new_registration, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        
    def test_add_registration_over_capacity_waiting_list(self):
        # Add class first
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        
        # make the capacity to 1
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 1,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        second_course = {
            'name': "B2A",
            'course_description': 'Morning session for grade 2nd class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=second_course, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Add student
        parent_account = self.create_user('parent', 'parent@gmail.com')
        self.create_member(parent_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        # Add two students
        first_student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/add-student/',
                                   data=first_student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        second_student_json = {
            'first_name': 'luke',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/add-student/',
                                   data=second_student_json, format='json')
        first_student = Student.objects.get(first_name="david")
        persisted_course = Course.objects.get(name="B1A")

        # Add registration
        payload = {
            'course_id': persisted_course.id,
            'student': {
                'first_name': first_student.first_name,
                'last_name': first_student.last_name,
                'date_of_birth': first_student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registration = Registration.objects.get(student=first_student)
        self.assertFalse(registration.on_waiting_list)

        # Second registration will be added to waiting list as the class can only hold one student.
        second_student = Student.objects.get(first_name="luke")

        payload = {
            'course_id': persisted_course.id,
            'student': {
                'first_name': second_student.first_name,
                'last_name': second_student.last_name,
                'date_of_birth': second_student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registration = Registration.objects.get(student=second_student)
        self.assertTrue(registration.on_waiting_list)


    def test_unregistration_succeed(self):
         # Add class first
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        persisted_course = Course.objects.get(name="B1A")
        # Add student
        parent_account = self.create_user('parent', 'parent@gmail.com')
        self.create_member(parent_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Member.objects.get(user_id=parent_account)
        student = Student.objects.get(parent_id=member)
        self.assertEqual(student.last_name, 'chatty')
        self.assertEqual(student.first_name, 'david')
        self.assertIsNotNone(student.joined_date)
        # Add registration
        payload = {
            'course_id': persisted_course.id,
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registration = Registration.objects.get(student=student)
        self.assertEqual(registration.course.name, "B1A")
        self.assertEqual(registration.student.last_name, student.last_name)
        self.assertEqual(registration.student.first_name, student.first_name)
        self.assertIsNotNone(registration.school_year_start)
        self.assertIsNotNone(registration.school_year_end)
        self.assertEqual(registration.registration_date.day, datetime.datetime.today().day)

        # make sure the student can also be searched 
        updated_course = Course.objects.get(name='B1A')
        self.assertEqual(len(updated_course.students.filter(first_name=student.first_name)), 1)

        unregister_url = '/rest_api/members/{registration_id}/unregister-course/'.format(
            registration_id = registration.id
        )
        response = self.client.put(unregister_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        updated_course = Course.objects.get(name='B1A')
        self.assertEqual(len(updated_course.students.filter(first_name=student.first_name)), 0)

    def test_update_registration_course_succeed(self):
        # Add class first
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        # Add two courses so that the user can udpate their registration.
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        another_course_json = {
            'name': "B2A",
            'course_description': 'Morning session for grade 2 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=another_course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        persisted_course = Course.objects.get(name="B1A")
        # Add student
        parent_account = self.create_user('parent', 'parent@gmail.com')
        self.create_member(parent_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        student_json = {
            'first_name': 'david',
            'last_name': 'chatty',
            'date_of_birth': '2015-10-01',
            'gender': 'M'
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/add-student/',
                                   data=student_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        member = Member.objects.get(user_id=parent_account)
        student = Student.objects.get(parent_id=member)
        self.assertEqual(student.last_name, 'chatty')
        self.assertEqual(student.first_name, 'david')
        self.assertIsNotNone(student.joined_date)
        # Add registration
        payload = {
            'course_id': persisted_course.id,
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registration = Registration.objects.get(student=student)
        self.assertEqual(registration.course.name, "B1A")
        self.assertEqual(registration.student.last_name, student.last_name)
        self.assertEqual(registration.student.first_name, student.first_name)
        self.assertIsNotNone(registration.school_year_start)
        self.assertIsNotNone(registration.school_year_end)
        self.assertEqual(registration.registration_date.day, datetime.datetime.today().day)

        # make sure the student can also be searched 
        updated_course = Course.objects.get(name='B1A')
        students = updated_course.students.filter(first_name=student.first_name)
        self.assertEqual(len(students), 1)

        # Update registration
        persisted_course = Course.objects.get(name="B2A")
        updated_payload = {
            'id': registration.id,
            'course': persisted_course.id,
            'student': registration.student.id,
            'school_year_start': registration.school_year_start,
            'school_year_end': registration.school_year_end,
            'registration_code': registration.registration_code,
            'registration_date': registration.registration_date
        }
        response = self.client.put('/rest_api/members/update-registration/',
                                   data=updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        # No op on the second request
        response = self.client.put('/rest_api/members/update-registration/',
                                   data=updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        updated_course = Course.objects.get(name='B2A')
        students = updated_course.students.filter(first_name=student.first_name)
        self.assertEqual(len(students), 1)

        updated_course = Course.objects.get(name='B1A')
        students = updated_course.students.filter(first_name=student.first_name)
        self.assertEqual(len(students), 0)
