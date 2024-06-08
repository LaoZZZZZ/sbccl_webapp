
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from rest_framework import status
from .models import Coupon, Member, Student, Course, Registration, Payment, InstructorAssignment, CouponUsageRecord, SchoolCalendar
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
import datetime
import json

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

    def createCoupon(self, coupon_code, application_rule, expiration_date):
        coupon = Coupon(type='A', dollar_amount=50, code=coupon_code,
                        application_rule=application_rule, creator='test',
                        expiration_date = expiration_date,
                        creation_date=datetime.date.today())
        coupon.save()
        return coupon

    def test_create_member_succeed(self):
        user_json = {'username': 'test_name', 'email': 'test4@gmail.com',
                      'first_name': 'Sandy', 'last_name': 'Zhao', 'password': 'Helloworld1',
                      'member_type': 'parent'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id.username, 'test_name')
        user = User.objects.get(username='test_name')
        created_member = Member.objects.get(user_id=user)
        self.assertEqual(created_member.sign_up_status, 'S')
        self.assertEqual(created_member.member_type, 'P')
    
    def test_create_teacher_succeed(self):
        user_json = {'username': 'test_name', 'email': 'test4@gmail.com',
                      'first_name': 'Sandy', 'last_name': 'Zhao', 'password': 'Helloworld1',
                      'member_type': 'teacher'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id.username, 'test_name')
        user = User.objects.get(username='test_name')
        created_member = Member.objects.get(user_id=user)
        self.assertEqual(created_member.sign_up_status, 'S')
        self.assertEqual(created_member.member_type, 'T')

        # Fetch the students
        self.client.force_authenticate(user=user)

        response = self.client.get('/rest_api/members/fetch-students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_parent_succeed(self):
        user_json = {'username': 'test_name', 'email': 'test4@gmail.com',
                      'first_name': 'Sandy', 'last_name': 'Zhao', 'password': 'Helloworld1',
                      'member_type': 'Parent'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id.username, 'test_name')
        user = User.objects.get(username='test_name')
        created_member = Member.objects.get(user_id=user)
        self.assertEqual(created_member.sign_up_status, 'S')
        self.assertEqual(created_member.member_type, 'P')

    def test_create_volunteer_succeed(self):
        user_json = {'username': 'test_name', 'email': 'test4@gmail.com',
                      'first_name': 'Sandy', 'last_name': 'Zhao', 'password': 'Helloworld1',
                      'member_type': 'Volunteer'}
        response = self.client.post('/rest_api/members/', data=user_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Member.objects.count(), 1)
        self.assertEqual(Member.objects.get().user_id.username, 'test_name')
        user = User.objects.get(username='test_name')
        created_member = Member.objects.get(user_id=user)
        self.assertEqual(created_member.sign_up_status, 'S')
        self.assertEqual(created_member.member_type, 'V')

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
            username='david@gmail.com',
            password='helloworld12H'
        )
        exist_user.email = "david@gmail.com"
        exist_user.save()

        user_json = {'username': 'david@gmail.com', 'password': 'helloworld12H',
                     'email': 'david@gmail.com', 'first_name': 'David', 'last_name': 'Rob'}
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

    def test_user_account_details_succeed(self):
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user)

        self.client.force_authenticate(user=exist_user)
        response = self.client.get('/rest_api/members/account-details/',format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('account_details' in response.data)


    def test_verify_user_succeed(self):
        verification_code = "12345-abc"
        exist_user = self.create_user('david@gmail.com', 'david@gmail.com')
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

        # Fetch the students
        response = self.client.get('/rest_api/members/fetch-students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


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
            'cost': 500,
            'classroom': 'N402',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
        self.assertEqual(persited_course.course_start_time, datetime.time(10, 0))
        self.assertEqual(persited_course.course_end_time, datetime.time(11, 50))

        updated_course = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class 2024.',
            'course_type': "L",
            'course_status': 'U',
            'size_limit': 1,
            'cost': 400,
            'classroom': 'S402'
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
            'cost': 500,
            'classroom': 'N402',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
        self.assertEqual(obtained_course['course_start_time'], '10:00:00')
        self.assertEqual(obtained_course['course_end_time'], '11:50:00')

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
            'cost': 500,
            'classroom': 'N101',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
        self.assertEqual(registration.expiration_date, registration.school_year_end)

        payment = Payment.objects.get(registration_code=registration)
        self.assertEqual(payment.payment_status, 'NP')
        # make sure the student can also be searched 
        updated_course = Course.objects.get(name='B1A')
        updated_course.students.get(first_name=student.first_name)

    def test_add_registration_course_with_coupon_succeed(self):
        coupon_code = 'EARLY_BIRD_2024'
        coupon = self.createCoupon(coupon_code, 'PA', expiration_date=datetime.date.today())
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
            'cost': 500,
            'classroom': 'N101',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00',
            'book_cost': 50
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
            },
            'coupon_code': coupon_code,
            'textbook_ordered': False
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
        self.assertEqual(registration.expiration_date, registration.school_year_end)
        self.assertFalse(registration.textbook_ordered)

        payment = Payment.objects.get(registration_code=registration)
        self.assertEqual(payment.payment_status, 'NP')
        
        # make sure the student can also be searched 
        updated_course = Course.objects.get(name='B1A')
        updated_course.students.get(first_name=student.first_name)

        response = self.client.get('/rest_api/members/account-details/',format='json')
        self.assertEqual(response.data['account_details']['balance'],
                         ''.join(['$', str(updated_course.cost - coupon.dollar_amount)]))

    def test_add_registration_enrichment_course_succeed(self):
        # Add class first
        board_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(board_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        # Add language class registration first.
        course_json = {
            'name': "B1A",
            'course_description': 'Morning session for grade 1 class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500,
            'classroom': 'N101',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
        }

        self.client.force_authenticate(user=board_user)
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
            },
            'textbook_ordered': False
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Add enrichment class registration
        course_json = {
            'name': "Go Beginner",
            'course_description': 'Enrichment class Go beginner.',
            'course_type': "E",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500,
            'classroom': 'N101',
            'course_start_time': '12:00:00',
            'course_end_time': '12:50:00'
        }

        self.client.force_authenticate(user=board_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        enrichment_persisted_course = Course.objects.get(name="Go Beginner")
        payload = {
            'course_id': enrichment_persisted_course.id,
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            },
            'textbook_ordered': False
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registration = Registration.objects.get(student=student, course__course_type='E')
        self.assertEqual(registration.course.name, "Go Beginner")
        self.assertEqual(registration.student.last_name, student.last_name)
        self.assertEqual(registration.student.first_name, student.first_name)
        self.assertIsNotNone(registration.school_year_start)
        self.assertIsNotNone(registration.school_year_end)
        self.assertEqual(registration.registration_date.day, datetime.datetime.today().day)
        self.assertEqual(registration.expiration_date, registration.school_year_end)
        self.assertFalse(registration.textbook_ordered)


    def test_add_registration_enrichment_course_failed(self):
        # Add class first
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='B')
        
        course_json = {
            'name': "Go Beginner",
            'course_description': 'Enrichment class Go beginner.',
            'course_type': "E",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500,
            'classroom': 'N101',
            'course_start_time': '12:00:00',
            'course_end_time': '12:50:00'
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        persisted_course = Course.objects.get(name="Go Beginner")
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
            },
            'textbook_ordered': False
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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
            'cost': 500,
            'classroom': 'N228'
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
            'cost': 500,
            'classroom': 'N442',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Second course has overlapped time window.
        second_course = {
            'name': "B2A",
            'course_description': 'Morning session for grade 2nd class.',
            'course_type': "L",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500,
            'classroom': 'N118',
            'course_start_time': '11:00:00',
            'course_end_time': '13:50:00'
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
            'cost': 500,
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
            'cost': 500,
            'classroom': 'N110'
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


    def test_promoted_from_waiting_list(self):
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
            'cost': 500,
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
            'cost': 500,
            'classroom': 'N110',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
        second_registration_payload = {
            'course_id': persisted_course.id,
            'student': {
                'first_name': first_student.first_name,
                'last_name': first_student.last_name,
                'date_of_birth': first_student.date_of_birth,
                'gender': 'M'
            }
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=second_registration_payload, format='json')
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
        waiting_list = Registration.objects.get(student=second_student)
        self.assertTrue(waiting_list.on_waiting_list)

        # Unregister the first student, the second should be automatically enrolled.
        unregister_url = '/rest_api/members/{registration_id}/unregister-course/'.format(
            registration_id = registration.id
        )
        response = self.client.put(unregister_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        updated_course = Course.objects.get(name='B1A')
        self.assertEqual(updated_course.students.count(), 1)
        registration = Registration.objects.get(student=second_student)
        self.assertFalse(registration.on_waiting_list)

    def test_unregistration_succeed(self):
        coupon_code = 'EARLY_BIRD_2024'
        coupon = self.createCoupon(coupon_code, 'PA', expiration_date=datetime.date.today())
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
            'cost': 500,
            'classroom': 'N116'
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
            },
            'coupon_code': coupon_code
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

        # make sure the coupon usage is also removed once the registration is removed.
        coupon_usage = CouponUsageRecord.objects.filter(user=member)
        self.assertTrue(len(coupon_usage) == 0)

    # 
    def test_unregistration_failed_with_enrichment_class_registration(self):
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
            'cost': 500,
            'classroom': 'N116',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
            },
        }
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        l_registration = Registration.objects.get(student=student)
        self.assertEqual(l_registration.course.name, "B1A")
        self.assertEqual(l_registration.student.last_name, student.last_name)
        self.assertEqual(l_registration.student.first_name, student.first_name)
        self.assertIsNotNone(l_registration.school_year_start)
        self.assertIsNotNone(l_registration.school_year_end)
        self.assertEqual(l_registration.registration_date.day, datetime.datetime.today().day)

        # make sure the student can also be searched 
        updated_course = Course.objects.get(name='B1A')
        self.assertEqual(len(updated_course.students.filter(first_name=student.first_name)), 1)
        # Add enrichment class registration
        course_json = {
            'name': "Go Beginner",
            'course_description': 'Enrichment class Go beginner.',
            'course_type': "E",
            'course_status': 'A',
            'size_limit': 20,
            'cost': 500,
            'classroom': 'N101',
            'course_start_time': '12:00:00',
            'course_end_time': '12:50:00'
        }

        self.client.force_authenticate(user=exist_user)
        response = self.client.put('/rest_api/members/upsert-course/',
                                   data=course_json, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        enrichment_persisted_course = Course.objects.get(name="Go Beginner")
        payload = {
            'course_id': enrichment_persisted_course.id,
            'student': {
                'first_name': student.first_name,
                'last_name': student.last_name,
                'date_of_birth': student.date_of_birth,
                'gender': 'M'
            },
            'textbook_ordered': False
        }
        self.client.force_authenticate(user=parent_account)
        response = self.client.put('/rest_api/members/register-course/',
                                   data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        unregister_url = '/rest_api/members/{registration_id}/unregister-course/'.format(
            registration_id = l_registration.id
        )
        response = self.client.put(unregister_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        updated_course = Course.objects.get(name='B1A')
        self.assertEqual(len(updated_course.students.filter(first_name=student.first_name)), 1)

    def test_update_registration_course_succeed(self):
        coupon_code = 'EARLY_BIRD_2025'
        coupon = self.createCoupon(coupon_code, 'PA', expiration_date=datetime.date.today())
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
            'cost': 500,
            'classroom': 'N108'
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
            'cost': 400
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
        payment = Payment.objects.get(registration_code=registration)
        self.assertEqual(payment.original_amount, updated_course.cost)

        # Update registration
        persisted_course = Course.objects.get(name="B2A")
        updated_payload = {
            'id': registration.id,
            'course': persisted_course.id,
            'student': registration.student.id,
            'school_year_start': registration.school_year_start,
            'school_year_end': registration.school_year_end,
            'registration_code': registration.registration_code,
            'registration_date': registration.registration_date,
            'coupons': [coupon_code]
        }
        response = self.client.put('/rest_api/members/update-registration/',
                                   data=updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        payment = Payment.objects.get(registration_code=registration)
        self.assertEqual(payment.original_amount, persisted_course.cost - coupon.dollar_amount)

        # can not apply the same coupon to the same registration repeatedly.
        response = self.client.put('/rest_api/members/update-registration/',
                                   data=updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # No op if there is no update.
        del updated_payload['coupons']
        response = self.client.put('/rest_api/members/update-registration/',
                                   data=updated_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        updated_course = Course.objects.get(name='B2A')
        students = updated_course.students.filter(first_name=student.first_name)
        self.assertEqual(len(students), 1)

        updated_course = Course.objects.get(name='B1A')
        students = updated_course.students.filter(first_name=student.first_name)
        self.assertEqual(len(students), 0)


    def test_fetch_students_for_teacher(self):
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
            'cost': 500,
            'classroom': 'N101',
            'course_start_time': '10:00:00',
            'course_end_time': '11:50:00'
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
        
        # Add teacher
        teacher_account = self.create_user('teacher', 'teacher@gmail.com')
        self.create_member(teacher_account, sign_up_status='V',
                           verification_code="12345-1231", member_type='T')
        user = User.objects.get(username='teacher')
        teacher_member = Member.objects.get(user_id=user)
        self.assertEqual(teacher_member.sign_up_status, 'V')
        self.assertEqual(teacher_member.member_type, 'T')

        
        assignment = InstructorAssignment()
        assignment.course = persisted_course
        assignment.instructor = teacher_member
        assignment.school_year_start = datetime.date(year=2023, month=9, day=1)
        assignment.school_year_end = datetime.date(year=2024, month=6, day=23)
        assignment.assigned_date = datetime.date.today()
        assignment.last_update_date=datetime.date.today()
        assignment.expiration_date = datetime.datetime.today() + datetime.timedelta(days=2)
        assignment.last_update_person="Test"
        assignment.save()

        # fetch students under the teacher
        self.client.force_authenticate(user=teacher_account)
        response = self.client.get('/rest_api/members/fetch-students/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('data' in response.data)
        self.assertEqual(len(response.data['data']), 1)
        self.assertTrue('students' in response.data['data'][0])
        self.assertTrue('course' in response.data['data'][0])


    def test__get_coupon_details_succeed(self):
        code = 'early_bird'
        self.createCoupon(code, 'PA', expiration_date=datetime.date.today())
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')

        self.client.force_authenticate(user=exist_user)
        response = self.client.get('/rest_api/members/{code}/coupon-details/'.format(code=code),
                                   format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        retrieved_coupon = json.loads(response.data)
        self.assertEqual(retrieved_coupon['code'], code)
        self.assertEqual(retrieved_coupon['dollar_amount'], 50)

    def test__get_coupon_details_failed(self):
        coupon_code = 'expired_code'
        self.createCoupon(coupon_code, application_rule='PA',
                          expiration_date=datetime.date.today() - datetime.timedelta(days=1))
        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        self.client.force_authenticate(user=exist_user)
        response = self.client.get('/rest_api/members/{code}/coupon-details/'.format(code=coupon_code),
                                   format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_get_coupon_details_unavailable(self):
    #     coupon_code = 'expired_code'
    #     saved_coupon = self.createCoupon(coupon_code, application_rule='PA',
    #                       expiration_date=datetime.date.today() - datetime.timedelta(days=1))
    #     exist_user = self.create_user('test_name', 'david@gmail.com')
    #     self.create_member(exist_user, sign_up_status='V',
    #                        verification_code="12345-1231", member_type='P')
    #     member = Member.objects.get(user_id=exist_user)
        
    #     usage = CouponUsageRecord(user=member, coupon=saved_coupon, registration=registration,
    #                               used_date=datetime.date.today())
    #     usage.save()
    #     self.client.force_authenticate(user=exist_user)
    #     response = self.client.get('/rest_api/members/{code}/coupon-details/'.format(code=coupon_code),
    #                                format='json')
        
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_get_calendar(self):
        day = SchoolCalendar()
        day.event = "School start"
        day.date = datetime.date.today()
        day.day_type = 'SD'
        day.school_year_end = day.date.year
        day.school_year_start = day.date.year - 1
        day.creation_date = datetime.date.today()
        day.last_update_date = datetime.datetime.today()
        day.last_update_person = 'test'
        day.save()

        expired_day = SchoolCalendar()
        expired_day.event = "School Start"
        expired_day.school_year_end = datetime.date.today().year - 1
        expired_day.school_year_start = datetime.date.today().year - 2
        expired_day.date = datetime.date.today().replace(year=expired_day.school_year_end)
        expired_day.creation_date = datetime.date.today().replace(year=expired_day.school_year_start)
        expired_day.last_update_date = expired_day.creation_date
        expired_day.last_update_person = 'test'
        expired_day.save()

        exist_user = self.create_user('test_name', 'david@gmail.com')
        self.create_member(exist_user, sign_up_status='V',
                           verification_code="12345-1231", member_type='P')
        self.client.force_authenticate(user=exist_user)
        response = self.client.get('/rest_api/members/fetch-calendar/', format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['calendar']), 1)
        fetched_dates = json.loads(response.data['calendar'][0])
        self.assertEqual(fetched_dates['school_year_start'], day.school_year_start)
        self.assertEqual(fetched_dates['school_year_end'], day.school_year_end)

        