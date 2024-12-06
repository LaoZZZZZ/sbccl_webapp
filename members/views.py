# For rest API
import datetime
import os
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives

from django.template import loader
from django.utils.html import strip_tags
import pytz
from rest_framework.viewsets import ModelViewSet

from .notification_utils import NotificationUtils
from .serializers import StudentSerializer, UserSerializer, MemberSerializer, CourseSerializer, PaymentSerializer, RegistrationSerializer, CouponSerializer, DropoutSerializer, SchoolCalendarSerializer
from .models import Course, Member, Student, Registration, Dropout, Payment, InstructorAssignment, Coupon, CouponUsageRecord, SchoolCalendar
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from members import models
import utils.validators.request_validator
from .coupon_utils import CouponUtils
from .balance_utils import BalanceUtils
from .calender_utils import find_current_school_year
import uuid
import json

from members import calender_utils

# REST APIs
class MemberViewSet(ModelViewSet):
    # all members
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    # The student can not unregister the last language class before remove themselves
    # from the active language class registration.
    def __need_unregister_enrichment_class(self, registration : Registration):
        student = registration.student
        language_registration = Registration.objects.filter(student=student,
                                                            course__course_type='L',
                                                            school_year_start__year=registration.school_year_start.year,
                                                            school_year_end__year=registration.school_year_end.year,
                                                            ).exclude(registration_code=registration.registration_code)
        
        if language_registration:
            return False
        # There is no other language class registration.
        enrichment_class = Registration.objects.filter(student=student,
                                                       course__course_type='E',
                                                       school_year_start__year=registration.school_year_start.year,
                                                       school_year_end__year=registration.school_year_end.year)
        return enrichment_class.count() >= 1

    # check if the student has language class registration.
    def __has_language_class_registration(self, persisted_student : Student, start_year : int,
                                          end_year: int):
        registrations = Registration.objects.filter(student=persisted_student,
                                                    course__course_type='L')
        for r in registrations:
            if r.school_year_start.year == start_year and r.school_year_end.year == end_year:
                return True
        return False

    # find the registration year
    def __find_registration_year(self, persisted_course : Course):
        return (persisted_course.school_year_start, persisted_course.school_year_end)

    # send email to board member about book ordering updates.
    def __email_for_textbook(self, registration: Registration):
        pass

    def __course_taught_by_teacher__(self, teacher: Member, course: Course):
        found = False
        for t in course.instructor.all():
            found = (t.user_id == teacher.user_id)
            if found:
                break
        return found
    

    def __get_all_coupons_per_registration(self, registration : Registration):
        coupons = []
        if not registration.coupons:
            return []
        for c in registration.coupons.all():
            coupons.append(CouponSerializer(c).data)
        return coupons
        
    # Set up the initial payment for new registration or update existing one if an registration
    # is updated.
    def __set_up_payment__(self, registration : Registration, member : Member, reg_date = None):
        payments = Payment.objects.filter(registration_code=registration)
        balance = self.__calculate_registration_due__(registration)
        if not payments:
            if balance == 0:
                return
            payment = Payment()
            payment.user = member
            payment.last_update_person = member.user_id.username
            payment.registration_code = registration
            payment.amount_in_dollar = 0
            # Temporarily set the pay date as today.
            if reg_date:
                payment.pay_date = reg_date
            else:
                payment.pay_date = datetime.date.today()
            payment.payment_status = 'NP'
        else:
            payment = payments[0]
        payment.original_amount = balance
        payment.last_udpate_date = datetime.date.today()
        payment.save()
            

    def __generate_unsuccessful_response(self, error_msg, status):
        return Response({'detail': error_msg}, status=status)

    def __generate_user_info__(self, user, member : Member, basic=False):
        user_info = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': member.phone_number
        }
        if not basic:
            user_info['member_type'] = member.getMemberType()
            if user.last_login:
                user_info['last_login'] = user.last_login.date()
            user_info['date_joined'] = user.date_joined.date()
            user_info['balance'] = '${amount}'.format(amount=self.__calculate_balance__(member))
            if member.term_signed_date:
                user_info['term_signed_date'] = member.term_signed_date
        return user_info

    def __get_teacher_infomation__(self, teacher_account):
        info = UserSerializer(teacher_account.user_id).data
        del info['password']
        return info

    def __generate_registration_info__(self, registration : Registration):
        payment = Payment.objects.filter(registration_code=registration)
        # Payment entry is generated upon registration. If there is no payment record,
        # it means the registration is free.
        if len(payment) == 1:
            payment_data = PaymentSerializer(payment[0]).data
        else:
            payment_data = None # Do not have the payment field
        return json.dumps({
            'student': StudentSerializer(registration.student).data,
            'registration': RegistrationSerializer(registration).data,
            'course': CourseSerializer(registration.course).data,
            'coupons': self.__get_all_coupons_per_registration(registration),
            'teacher': [self.__get_teacher_infomation__(teacher) for teacher in registration.course.instructor.all() if teacher.member_type == 'T'],
            # TODO: Remove this field once balance field is in back end.
            'payments': payment_data,
            'balance': 0 if not payment else BalanceUtils.CalculateBalance(registration, payment[0])
            })
    
    def __generate_dropout_info__(self, dropout : Dropout):
        payment = Payment.objects.filter(dropout_info=dropout)

        return json.dumps({
            'student': StudentSerializer(dropout.student).data,
            'dropout': DropoutSerializer(dropout).data,
            'balance': 0 if not payment else BalanceUtils.CalculateRefund(dropout, payment[0])
            })

    def __calculate_registration_due__(self, registration : Registration):
        coupon_usages = CouponUsageRecord.objects.filter(registration=registration)
        return CouponUtils.applyCoupons(registration.course.cost  + (registration.course.book_cost if registration.textbook_ordered else 0),
                                        [(u.coupon, u.used_date) for u in coupon_usages])

    def __calculate_balance__(self, member):
        students = Student.objects.filter(parent_id=member)
        balance = 0.0
        for s in students:
            registrations = Registration.objects.filter(student=s)
            for r in registrations:
                balance += self.__calculate_registration_due__(r)
                payment = Payment.objects.filter(registration_code=r.id)
                for p in payment:
                    balance -= p.amount_in_dollar
        return balance

    def __validate_member_type__(self, member_type):
        if not member_type:
            return None
        m = member_type.lower()
        if m == 'parent':
            return 'P'
        elif m == 'teacher':
            return 'T'
        elif m == 'volunteer':
            return 'V'
        else:
            return None

    # Retrieve all registrations for a member
    def __get_per_parent_registration__(self, matched_members):
        if matched_members.member_type != 'P':
            return ([], [])
        students = models.Student.objects.filter(parent_id=matched_members)
        registrations = []
        for s in students:
            matched_registrations = Registration.objects.filter(student=s)
            registrations = registrations + [self.__generate_registration_info__(r) for r in matched_registrations]
        return registrations

    # Retrieve all dropouts for a member
    def __get_per_parent_dropouts__(self, matched_members):
        if matched_members.member_type != 'P':
            return ([], [])
        students = models.Student.objects.filter(parent_id=matched_members)
        dropouts = []
        for s in students:
            matched_dropouts = Dropout.objects.filter(student=s)
            dropouts = dropouts + [self.__generate_dropout_info__(d) for d in matched_dropouts]
        return dropouts
    
    def __send_account_creation_html_email__(self, new_user, new_member, verification_url):
        """
        Send account creation confirmation email.
        """
        if new_member.member_type == 'P':
            html_message = loader.render_to_string("account_registration_email.html",
                                                  {'verification_link': verification_url})
            subject = 'Registration confirmation'
            plain_message = strip_tags(html_message)
            send_mail(subject, plain_message, from_email=None, recipient_list=[new_user.email],
                      html_message=html_message)

    def __get_students_per_course__(self, course : Course):
        """
          Find all students that register the course
        """
        all_students = []

        for student in course.students.all():
            data = StudentSerializer(student).data
            data['age'] = StudentSerializer.calculateAge(student.date_of_birth)
            del data['date_of_birth']
            p_user =  student.parent_id.user_id
            data['contact'] = JSONRenderer().render({
                'parent': ' '.join([p_user.first_name, p_user.last_name]),
                'email': p_user.email,
                'phone': student.parent_id.phone_number
            })
            # Retrive the registration status
            reg = Registration.objects.get(course=course, student=student)
            data['on_waiting_list'] = reg.on_waiting_list
            all_students.append(JSONRenderer().render(data))
        return all_students

    def __get_volunteers_per_course__(self, course : Course):
        """
        Find all TAs for the course
        """
        all_tas = []
        for ta in course.instructor.all():
            # only care about the instructor with volunteer member type.
            if ta.member_type == 'V':
                all_tas.append(JSONRenderer().render(
                    self.__generate_user_info__(user=ta.user_id, member=ta, basic=True)))
        return all_tas



    def __fetch_coupon__(self, user, coupon_code, registration=None):
        """
         Fetch the corresponding coupon and validate the coupon 
        """
        matched_coupon = Coupon.objects.get(code=coupon_code)
        # expired coupon can not be used.
        if not CouponUtils.IsValid(matched_coupon):
            raise ValueError("The coupon code ({code}) has expired!".format(code=matched_coupon.code))
        
        # Check if coupon can be applied to this account or the registration.
        matched_member = Member.objects.get(user_id=user)
        coupon_usages = CouponUsageRecord.objects.filter(user=matched_member)
        if not CouponUtils.canBeUsed(matched_coupon, coupon_usages, registration):
            raise ValueError("The coupon code ({code}) has been used!".format(code=matched_coupon.code))
        return matched_coupon

    def __record_coupon_usage__(self, coupon, registration, matched_member, apply_date = None):
        """
          Records the usage of this coupon by the user
        """
        # only keep one coupon for the registration.
        coupon_usage = CouponUsageRecord.objects.filter(registration = registration)
        if coupon_usage:
            for used_coupon in coupon_usage:
                used_coupon.delete()
        coupon_usage = CouponUsageRecord()
        if not apply_date:
            coupon_usage.used_date = datetime.date.today()
        else:
            coupon_usage.used_date = apply_date
        coupon_usage.user = matched_member
        coupon_usage.coupon = coupon
        coupon_usage.registration = registration
        coupon_usage.save()

    # These two course time window has overlap
    def __has_conflict__(self, course_a, course_b):
        return ((course_a.course_start_time >= course_b.course_start_time and course_a.course_start_time <= course_b.course_end_time)
            or (course_a.course_end_time >= course_b.course_start_time and course_a.course_end_time <= course_b.course_end_time))


    def __send_registration_email__(self, user, registration):
        html_message = loader.render_to_string("course_registration_email.html",
                                               {'registration': RegistrationSerializer(registration).data,
                                                'account_url': os.environ["FRONTEND_URL"],
                                                'student': ' '.join([registration.student.first_name, registration.student.last_name]),
                                                'class_name': registration.course.name,
                                                'school_start': registration.school_year_start.year,
                                                'school_end': registration.school_year_end.year,
                                                'status': "On Waiting List" if registration.on_waiting_list else "Enrolled",
                                                "balance": "$" + str(self.__calculate_registration_due__(registration))})
        subject = 'Class Registration confirmation'
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email=None, recipient_list=[user.email],
                  html_message=html_message)
       


    def __send_unregistration_email__(self, user, registration, payment: Payment,
                                      old_course=None):
        html_message = loader.render_to_string("course_unregistration_email.html",
                                               {'account_url': os.environ["FRONTEND_URL"],
                                                'student': ' '.join([registration.student.first_name, registration.student.last_name]),
                                                'class_name': old_course.name if old_course else registration.course.name,
                                                'school_start': registration.school_year_start.year,
                                                'school_end': registration.school_year_end.year})
        subject = 'Class withdraw confirmation'
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(
            subject=subject, body=plain_message, from_email=None, to=[user.email])
        if payment and payment.payment_status in ('FP', 'PP'):
            if "SCHOOL_ADMIN_EMAIL" in os.environ:
                email.cc.append(os.environ["SCHOOL_ADMIN_EMAIL"])
        email.attach_alternative(html_message, 'text/html')
        email.send()

    def __update_waiting_list__(self, course):
        waiting_list = []
        enrollment_size = 0
        registrations = Registration.objects.filter(course=course)
        for r in registrations:
            if r.on_waiting_list:
                waiting_list.append(r)
            else:
                enrollment_size += 1
        sorted(waiting_list, key=lambda registration:registration.registration_date)
        index = 0
        while enrollment_size <= course.size_limit and index < len(waiting_list):
            waiting_list[index].on_waiting_list = False
            waiting_list[index].save()
            parent = waiting_list[index].student.parent_id.user_id
            self.__email_waiting_list_removal__(parent, waiting_list[index])
            enrollment_size += 1


    def __email_waiting_list_removal__(self, user, registration):
        html_message = loader.render_to_string(
            "waiting_list_update_email.html",
            {
                'registration': RegistrationSerializer(registration).data,
                'account_url': os.environ["FRONTEND_URL"],
                'student': ' '.join([registration.student.first_name, registration.student.last_name]),
                'class_name': registration.course.name,
                'school_start': registration.school_year_start.year,
                'school_end': registration.school_year_end.year,
            })
        subject = 'Class Registration confirmation'
        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email=None, recipient_list=[user.email],
                  html_message=html_message)

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAdminUser()]
        elif self.action in ("create", "verify_user", "create_password_reset_code",
                             "reset_password_by_code"):
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        new_user = None
        try:
            existing_user = User.objects.filter(username=request.data['email'])
            if existing_user:
                return self.__generate_unsuccessful_response(
                    "This email address has been registered!", status=status.HTTP_409_CONFLICT)
            serialized = UserSerializer(data=request.data)
            if not serialized.is_valid():
                return self.__generate_unsuccessful_response("Invalid data is provided", status=status.HTTP_400_BAD_REQUEST)

            member_type = self.__validate_member_type__(request.data['member_type'])
            if not member_type:
                return self.__generate_unsuccessful_response(
                    "Invalid account type is not provided!", status=status.HTTP_400_BAD_REQUEST)

            if 'phone_number' in request.data:
                if not utils.validators.request_validator.ValidatePhoneNumber(request.data['phone_number']):
                    return self.__generate_unsuccessful_response(
                        "Invalid phone number is provided", status=status.HTTP_400_BAD_REQUEST)
                
            new_user = serialized.create(serialized.validated_data)
            registration_code = str(uuid.uuid5(uuid.NAMESPACE_URL, new_user.username))
            new_user.save()

            new_member = Member.objects.create(
                user_id=new_user,
                sign_up_status='S',
                verification_code=registration_code,
                member_type=member_type)
            if 'phone_number' in request.data:
                new_member.phone_number = request.data['phone_number']
            verification_url = os.path.join(os.environ["FRONTEND_URL"], "verify-user", registration_code)
            self.__send_account_creation_html_email__(new_user, new_member, verification_url)
            new_member.save()

            content = {
                'user': serialized.validated_data,
                'auth': None,
                'verification_url': verification_url
            }
            response = Response(data=content, status=status.HTTP_201_CREATED)
            response['location'] = registration_code
            return response
        except Exception as e:
            # User can not login for unverified account. Delete the user so that the user can retry.
            if new_user:
                new_user.delete()
            return self.__generate_unsuccessful_response("Account creation failed: " + str(e),
                                                         status.HTTP_400_BAD_REQUEST)


    @action(methods=['PUT'], detail=False, url_path='login', name='login user',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def login(self, request):
        try:
            matched_member = models.Member.objects.get(user_id=request.user)
            if matched_member.sign_up_status == 'S':
                return self.__generate_unsuccessful_response(
                    '{username} needs to be verified before login!'.format(username=matched_member.user_id.username),
                    status.HTTP_401_UNAUTHORIZED)
            login(request, request.user)
            user = User.objects.get(username=request.user)
            content = {
                'user': self.__generate_user_info__(user, matched_member),
                'auth': str(request.auth)
            }
            return Response(content, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist: 
            return self.__generate_unsuccessful_response(
                '{username} does not exist'.format(username=request.user.username),
                status.HTTP_404_NOT_FOUND)
        except Member.DoesNotExist:
            return self.__generate_unsuccessful_response(
                '{username} does not exist'.format(username=request.user.username),
                status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return self.__generate_unsuccessful_response('Encountered unexpected login error',
                                                         status.HTTP_500_INTERNAL_SERVER_ERROR)


    @action(methods=['PUT'], detail=True, url_path='logout', name='log out user',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def logout(self, request, pk=None):
        try:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist or models.Member.DoesNotExist:
            return self.__generate_unsuccessful_response("No user is found", status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path='account-details', name='Account details',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def account_details(self, request):
        try:
            matched_member = models.Member.objects.get(user_id=request.user)
            if matched_member.sign_up_status == 'S':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(username=request.user)
            content = {
                'account_details': self.__generate_user_info__(user, matched_member)
            }
            return Response(content, status=status.HTTP_200_OK)
        except (User.DoesNotExist, models.Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response("No user is found", status.HTTP_404_NOT_FOUND)
    
    @action(methods=['PUT'], detail=False, url_path='sign-terms', name='Sign CCL agreements',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def sign_terms(self, request):
        try:
            matched_member = models.Member.objects.get(user_id=request.user)
            matched_member.term_signed_date = datetime.date.today()
            if matched_member.sign_up_status == 'S':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            matched_member.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except (User.DoesNotExist, models.Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response("No user is found", status.HTTP_404_NOT_FOUND)

    """
     Verify the signup for the user.
    """
    @action(methods=['PUT'], detail=False, url_path='verify-user', name='Verify the user.',
            authentication_classes=[],
            permission_classes=[permissions.AllowAny])
    def verify_user(self, request):
        verification_code = request.query_params.get('verification_code')
        email = request.query_params.get('email')
        if verification_code is None or verification_code == '':
            return self.__generate_unsuccessful_response(
                "No verification code is provided!",
                status=status.HTTP_400_BAD_REQUEST)
        if email is None:
            return self.__generate_unsuccessful_response(
                "No email was provided!", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=email)
            matched_members = models.Member.objects.get(user_id=user.id)
            # User has already been verified
            if matched_members.sign_up_status == 'V':
                return self.__generate_unsuccessful_response(
                    "The user has already been verified!", status.HTTP_409_CONFLICT)
            if matched_members.verification_code != verification_code:
                self.__generate_unsuccessful_response(
                    "Incorrect verification code is provided!",status=status.HTTP_400_BAD_REQUEST)
            # Send verification email
            if matched_members.member_type != 'P':
                send_mail(
                    subject="Account is verified",
                    message="The account registered with {email} has been verified. You can start using your account now. Congratulations!".format(email=user.email),
                    from_email="no-reply@sbcclny.com",
                    recipient_list=[user.email, 'ccl_admin@sbcclny.com'])
            matched_members.sign_up_status = 'V'
            matched_members.verification_code = None
            matched_members.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist as e:
            return self.__generate_unsuccessful_response(
                'There is no user registered with - ' + email, status.HTTP_404_NOT_FOUND)
        except Member.DoesNotExist as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_404_NOT_FOUND)

    """
    User forget password. They want to reset the password via a randomly generated code
    """
    @action(methods=['PUT'], detail=False, url_path='create-password-reset-code',
            name='Verify the user.',
            authentication_classes=[],
            permission_classes=[permissions.AllowAny])
    def create_password_reset_code(self, request):
        try:
            email_address = request.query_params.get('email')
            retrieved_user = User.objects.get(email=email_address)
            matched_members = Member.objects.filter(user_id=retrieved_user)
            if not matched_members:
                return self.__generate_unsuccessful_response(
                    "The user does not exist!", status.HTTP_404_NOT_FOUND)
            registration_code = str(uuid.uuid5(uuid.NAMESPACE_URL, retrieved_user.username))

            for m in matched_members:
                m.verification_code = registration_code
                m.save()
            verification_url = os.path.join(os.environ["FRONTEND_URL"], "reset-password-by-code", registration_code)
            msg = "You just requested to reset your password. Please click {link} to reset your password.".format(link=verification_url)
            retrieved_user.email_user(
                subject="Password reset",
                message=msg)
            response = Response(status=status.HTTP_201_CREATED)
            response['location'] =registration_code
            return response
        except ValidationError:
            return self.__generate_unsuccessful_response(status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return self.__generate_unsuccessful_response(
                "{username} does not exist!".format(username=email_address),
                status.HTTP_404_NOT_FOUND)

    """
    User forget password. They want to reset the password via
    """
    @action(methods=['PUT'], detail=False, url_path='reset-password-by-code',
            name='Reset password.',
            authentication_classes=[BasicAuthentication],
            permission_classes=[permissions.AllowAny])
    def reset_password_by_code(self, request):
        verification_code = request.query_params.get('verification_code')
        if verification_code is None:
            return self.__generate_unsuccessful_response(
                'No verification code is provided!', status.HTTP_400_BAD_REQUEST)
        new_password = request.query_params.get('password')
        if new_password is None:
            return self.__generate_unsuccessful_response(
                'No password is provided!', status.HTTP_400_BAD_REQUEST)
        try:
            email_address = request.query_params.get('email')
            retrieved_user = User.objects.get(email=email_address)
            matched_member = Member.objects.get(user_id=retrieved_user)
            validated_pass = UserSerializer().validate_password(new_password)
            if matched_member.verification_code != verification_code:
                return Response("Invalid verification code is provided!",
                                status=status.HTTP_400_BAD_REQUEST)
            retrieved_user.set_password(validated_pass)
            retrieved_user.save()
            matched_member.verification_code = None
            matched_member.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except ValidationError as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return self.__generate_unsuccessful_response(
                "{email} is not registered".format(email=request.query_params.get('email')),
                status.HTTP_404_NOT_FOUND)

    """
    Reset the password for the user.
    """
    @action(methods=['PUT'], detail=False, url_path='reset-password', name='Reset password.',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def reset_password(self, request, pk=None):
        new_password = request.query_params.get('new_password')
        if new_password is None:
            return self.__generate_unsuccessful_response(
                "Invalid password is provided", status.HTTP_400_BAD_REQUEST)
        try:
            validated_pass = UserSerializer().validate_password(new_password)
            user = User.objects.get(username=request.user.username)
            user.password = validated_pass
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return self.__generate_unsuccessful_response(
                "Invalid password is provided", status.HTTP_400_BAD_REQUEST)

        
    @action(methods=['PUT'], detail=False, url_path='add-student', name='Add student to the member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def add_student(self, request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return self.__generate_unsuccessful_response(
                    JSONRenderer().render(serializer.errors), status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            # Only parent can add students.
            if matched_member.member_type != 'P':
                return self.__generate_unsuccessful_response(
                    "Only parent can add students!", status.HTTP_400_BAD_REQUEST)
            new_student = serializer.create(serializer.validated_data)
            existing_students = Student.objects.filter(parent_id=matched_member)
            for s in existing_students:
                if s.first_name.upper() == new_student.first_name.upper() and s.last_name.upper() == new_student.last_name.upper():
                    return self.__generate_unsuccessful_response("The student already exists!", status.HTTP_409_CONFLICT)
            new_student.parent_id = matched_member
            new_student.save()
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return self.__generate_unsuccessful_response("No user is found!", status.HTTP_404_NOT_FOUND)

    @action(methods=['PUT'], detail=False, url_path='update-student', name='Update an existing student',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def update_student(self, request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return self.__generate_unsuccessful_response(
                    JSONRenderer().render(serializer.errors), status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            
            existing_students = Student.objects.filter(parent_id=matched_member)
            matched_student = None
            updated_student_info = serializer.validated_data
            for s in existing_students:
                if s.first_name.upper() == updated_student_info['first_name'].upper() and s.last_name.upper() == updated_student_info['last_name'].upper():
                    matched_student = s
                    break
            if not matched_student:
                return self.__generate_unsuccessful_response(
                    "The student does not exist!", status=status.HTTP_400_BAD_REQUEST)
            if 'date_of_birth' in updated_student_info:
                matched_student.date_of_birth = updated_student_info['date_of_birth']
            if 'middle_name' in updated_student_info:
                matched_student.middle_name = updated_student_info['middle_name']
            if 'chinese_name' in updated_student_info:
                matched_student.chinese_name = updated_student_info['chinese_name']
            if 'gender' in updated_student_info:
                matched_student.gender = updated_student_info['gender']
            matched_student.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return self.__generate_unsuccessful_response("No user is found!", status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return self.__generate_unsuccessful_response("Invalid student information!",
                                                         status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False, url_path='remove-student', name='Remove student from member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def remove_student(self, request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            student_to_delete = serializer.create(serializer.validated_data)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            # Only parent can remove students.
            if matched_member.member_type != 'P':
                return self.__generate_unsuccessful_response(
                    "Only parent can remove students!", status.HTTP_400_BAD_REQUEST)
            existing_students = Student.objects.filter(parent_id=matched_member,
                                                       first_name=student_to_delete.first_name,
                                                       last_name=student_to_delete.last_name)
            if not existing_students:
                return self.__generate_unsuccessful_response(
                    "The student does not exist!", status.HTTP_400_BAD_REQUEST)
            for s in existing_students:
                registration = Registration.objects.filter(student=s)
                if registration:
                    return self.__generate_unsuccessful_response(
                        """The student still has active enrollments! Please remove their enrollments first on the registration page before removing the student!""",
                        status.HTTP_400_BAD_REQUEST)
                s.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path='fetch-students',
            name='Get all students for the member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def fetch_students(self, request, pk=None):
        """
         Fetch students for parent account
        """
        try:
            user = User.objects.get(username=request.user)
            matched_member = models.Member.objects.get(user_id=user)
            students = []
            # Fetch relevant students for different type of member
            if matched_member.member_type != 'P':
                return self.__generate_unsuccessful_response(
                    "Non-parent account can not access all students",
                    status=status.HTTP_403_FORBIDDEN)
            students = models.Student.objects.filter(parent_id=matched_member)
            content = {
                'students': [JSONRenderer().render(StudentSerializer(s).data) for s in students]
            }
            
            return Response(data=content, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Member.DoesNotExist):
            return self.__generate_unsuccessful_response(
                'There is no user registered with - ' + request.user,
                status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=True, url_path='list-students-per-class',
            name='Get all students for a class',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def list_students(self, request, pk=None):
        """
          Fetch all students in this class.
        """
        try:
            user = User.objects.get(username=request.user)
            matched_member = models.Member.objects.get(user_id=user)
            if matched_member.member_type == 'P':
                return self.__generate_unsuccessful_response(
                    "Parent account has no access to a class roster!", status.HTTP_403_FORBIDDEN)
            persisted_class = Course.objects.get(id=pk)
            # Teacher can only see the roster of their own classes
            if matched_member.member_type == 'T':
                found = False
                for instructor in persisted_class.instructor.all():
                    if instructor.user_id == user:
                        found = True
                        break
                if not found:
                    return self.__generate_unsuccessful_response(
                    "You don't have access to the roster of this class!", status.HTTP_403_FORBIDDEN)
            content = {
                'students': self.__get_students_per_course__(persisted_class)
            }
            return Response(data=content, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(
                'There is no user registered with - ' + request.user,
                status.HTTP_404_NOT_FOUND)
        except (Course.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(
                'There is no such class with id = ' + pk,
                status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=True, url_path='list-volunteers-per-class',
            name='Get all volunteers for a class',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def list_volunteers(self, request, pk=None):
        """
          Fetch all volunteers for this class. Mostly teaching assistants.
        """
        try:
            user = User.objects.get(username=request.user)
            matched_member = models.Member.objects.get(user_id=user)
            if matched_member.member_type == 'P':
                return self.__generate_unsuccessful_response(
                    "Parent account has no access to volunteers in a class!", status.HTTP_403_FORBIDDEN)
            persisted_class = Course.objects.get(id=pk)
            # Teacher can only see the volunteers of their own classes
            if matched_member.member_type == 'T':
                found = False
                for instructor in persisted_class.instructor.all():
                    if instructor.user_id == user:
                        found = True
                        break
                if not found:
                    return self.__generate_unsuccessful_response(
                        "You don't have no access to volunteers in a class!", status.HTTP_403_FORBIDDEN)
            content = {
                'volunteers': self.__get_volunteers_per_course__(persisted_class)
            }
            return Response(data=content, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(
                'There is no user registered with - ' + request.user,
                status.HTTP_404_NOT_FOUND)
        except (Course.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(
                'There is no such class with id = ' + pk,
                status.HTTP_404_NOT_FOUND)

    # list all registrations that associate with the user. If the user is board member, all registration
    # would be returned with pagination.
    @action(methods=['GET'], detail=False, url_path='list-registrations',
            name='Get all students for the member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def list_registrations(self, request):
        try:
            user = User.objects.get(username=request.user)
            matched_members = models.Member.objects.get(user_id=user)
            registrations = self.__get_per_parent_registration__(matched_members)
            content = {
                'registrations': registrations,
            }
            return Response(data=content, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(
                'There is no user registered with - ' + request.user,
                status.HTTP_404_NOT_FOUND)

    # list all registrations that associate with the user. If the user is board member, all registration
    # would be returned with pagination.
    @action(methods=['GET'], detail=False, url_path='list-dropouts',
            name='Get all course dropouts for the member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def list_dropouts(self, request):
        try:
            user = User.objects.get(username=request.user)
            matched_members = models.Member.objects.get(user_id=user)
            dropouts = self.__get_per_parent_dropouts__(matched_members)
            content = {
                'dropouts': dropouts
            }
            return Response(data=content, status=status.HTTP_200_OK)
        except (User.DoesNotExist, Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(
                'There is no course dropouts with - ' + request.user,
                status.HTTP_404_NOT_FOUND)


    @action(methods=['PUT'], detail=False, url_path='register-course', name='Register a student to a course',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def register_course(self, request):
        try:
            coupon = None
            if 'coupon_code' in request.data and len(request.data['coupon_code']) > 0:
                coupon = self.__fetch_coupon__(request.user, request.data['coupon_code'])
                
            course_id = request.data['course_id']
            if not course_id:
                return self.__generate_unsuccessful_response(
                    "No course is provided", status.HTTP_400_BAD_REQUEST)
            persisted_course = Course.objects.get(id=course_id)
            if persisted_course.course_status != 'A':
                return self.__generate_unsuccessful_response(
                    "The class is no longer open for registration", status.HTTP_400_BAD_REQUEST)
            student_serializer = StudentSerializer(data=request.data['student'])
            if not student_serializer.is_valid():
                return self.__generate_unsuccessful_response("Invalid student is provided", status.HTTP_400_BAD_REQUEST)
            validated = student_serializer.validated_data

            user = User.objects.get(username=request.user)
            matched_member = models.Member.objects.get(user_id=user)
            persisted_student = Student.objects.get(first_name=validated['first_name'],
                                                    last_name=validated['last_name'],
                                                    parent_id=matched_member)
            
            matched_registration = Registration.objects.filter(student=persisted_student)
            for m in matched_registration:
                if self.__has_conflict__(m.course, persisted_course) and m.course.course_status == 'A':
                    return self.__generate_unsuccessful_response(
                        "The student already registered a same type of course!", status.HTTP_409_CONFLICT)

            start_year, end_year = self.__find_registration_year(persisted_course)
            # Need to check if the student can register enrichment class
            if persisted_course.course_type == 'E' and not self.__has_language_class_registration(persisted_student, start_year, end_year):
                return self.__generate_unsuccessful_response(
                    "The student must first register Language class before registering Enrichment class!",
                    status.HTTP_400_BAD_REQUEST)

            registration = Registration()
            registration.registration_code = str(uuid.uuid5(uuid.NAMESPACE_OID,
                                                            persisted_student.first_name + persisted_student.last_name + persisted_course.name + user.email))
            registration.on_waiting_list = persisted_course.size_limit <= persisted_course.students.count()
            
            registration.course = persisted_course
            registration.student = persisted_student

            registration.school_year_start = datetime.date(year=start_year,
                                                           month=9, day = 1)
            registration.school_year_end = registration.school_year_start.replace(year=end_year,
                                                                                  month=7)
            registration.registration_date = datetime.date.today()
            registration.expiration_date = registration.school_year_end
            registration.last_update_date = registration.registration_date
            if 'textbook_ordered' in request.data:
                registration.textbook_ordered = request.data['textbook_ordered']
            # Set up a payment entry
            registration.save()
            if coupon:
                self.__record_coupon_usage__(coupon, registration, matched_member)
            self.__send_registration_email__(user, registration)
            self.__set_up_payment__(registration, matched_member)
            return Response(status=status.HTTP_201_CREATED)
        except (User.DoesNotExist, Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_404_NOT_FOUND)
        except (ValueError, Student.DoesNotExist, Course.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            registration.delete()
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False, url_path='update-registration', name='Update a registration',
        authentication_classes=[SessionAuthentication, BasicAuthentication],
        permission_classes=[permissions.IsAuthenticated])
    def update_registration(self, request):
        try:
            registration_serializer = RegistrationSerializer(data=request.data)
            if not registration_serializer.is_valid():
                return self.__generate_unsuccessful_response(
                    "Received invalid registration object!", status.HTTP_400_BAD_REQUEST)
            
            registraion_id = int(request.data['id'])
            matched_registration = Registration.objects.get(id = registraion_id)
            new_course_id = int(request.data['course'])
            if not new_course_id:
                return self.__generate_unsuccessful_response(
                    "No course is provided", status.HTTP_400_BAD_REQUEST)
            
            member = Member.objects.get(user_id=request.user)
            if 'coupons' in request.data and len(request.data['coupons']) > 0:
                if len(request.data['coupons']) > 1:
                    return self.__generate_unsuccessful_response(
                        "Only one coupon can be accepted at a time!", status.HTTP_400_BAD_REQUEST)
                # A new coupon is applied in this request, record the coupon usage
                if not isinstance(request.data['coupons'][0], int):
                    coupon = self.__fetch_coupon__(request.user, request.data['coupons'][0], matched_registration)
                    self.__record_coupon_usage__(coupon, matched_registration, member)
            
            if 'textbook_ordered' in registration_serializer.validated_data:
                if matched_registration.textbook_ordered != registration_serializer.validated_data['textbook_ordered']:
                    self.__email_for_textbook(matched_registration)
                matched_registration.textbook_ordered = registration_serializer.validated_data['textbook_ordered']

            # No change to the class, but still need to save updates in other fields.
            if matched_registration.course.id == new_course_id:
                matched_registration.last_update_date = datetime.datetime.today()
                matched_registration.save()
                self.__set_up_payment__(matched_registration, member)
                return Response(status=status.HTTP_202_ACCEPTED)
            
            new_course = Course.objects.get(id=new_course_id)
            if new_course.course_status != 'A':
                return self.__generate_unsuccessful_response(
                    "The selected class ({name}) is no longer open for registration".format(name=new_course.name),
                    status.HTTP_400_BAD_REQUEST)
            # Registration can only be updated for the same type of class.     
            if new_course.course_type != matched_registration.course.course_type:
                return self.__generate_unsuccessful_response(
                    "The registration is for {old_type} class. If you're interested in {new_type} class, please submit a new registration!".format(
                    old_type=matched_registration.course.course_type, new_type=new_course.type),
                    status.HTTP_400_BAD_REQUEST)
            old_course = matched_registration.course
            matched_registration.course = new_course
            matched_registration.last_update_date = datetime.datetime.today()
            matched_registration.on_waiting_list = new_course.size_limit >= new_course.students.count()
            matched_registration.save()
            self.__set_up_payment__(matched_registration, member)
            user = User.objects.get(username=request.user)
            self.__send_unregistration_email__(user, matched_registration, payment=None, old_course=old_course)
            self.__send_registration_email__(user, matched_registration)
            self.__update_waiting_list__(old_course)
            return Response(status=status.HTTP_202_ACCEPTED)
        except (User.DoesNotExist, Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_404_NOT_FOUND)
        except (ValueError, Student.DoesNotExist, Course.DoesNotExist, Coupon.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)


    @action(methods=['PUT'], detail=True, url_path='unregister-course', name='Unregister a student to a course',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def unregister_course(self, request, pk=None):
        try:
            matched_registration = Registration.objects.get(id=pk)
            if matched_registration.course.course_type == 'L' and self.__need_unregister_enrichment_class(matched_registration):
                return self.__generate_unsuccessful_response(
                    'The student registers an Enrichment class. Please unregster enrichment class before quitting Language class.',
                    status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=request.user)
            persited_member = Member.objects.get(user_id=user)
            persisted_payment = Payment.objects.filter(registration_code=matched_registration)
            if persisted_payment:
                if len(persisted_payment) > 1:
                    return Response("There are more than one payments associated with this registration!",
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                if persisted_payment[0].payment_status != 'NP':
                    # Only create dropout record if there is a payment record. Dropout record is designed
                    # to track refund and followup if needed.
                    dropout = Dropout()
                    dropout.dropout_date = datetime.datetime.today()
                    dropout.student =  matched_registration.student
                    dropout.original_registration_code = matched_registration.registration_code
                    dropout.user = persited_member
                    dropout.course_name = matched_registration.course.name
                    dropout.school_year_end = matched_registration.school_year_end
                    dropout.school_year_start = matched_registration.school_year_start
                    dropout.save()

                    persisted_payment[0].dropout_info = dropout
                    persisted_payment[0].last_udpate_date = dropout.dropout_date
                    persisted_payment[0].last_update_person = user.username
                    persisted_payment[0].save()
                else:
                    # Delete the payment record if no payment is made for this registration.
                    persisted_payment[0].delete()
            payment = persisted_payment[0] if persisted_payment else None
            self.__send_unregistration_email__(user, matched_registration, payment)
            if not matched_registration.on_waiting_list:
                self.__update_waiting_list__(matched_registration.course)

            matched_registration.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except (User.DoesNotExist, Member.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(
                'There is no user registered with - ' + request.user, status.HTTP_404_NOT_FOUND)
        except (Registration.DoesNotExist, Student.DoesNotExist, Course.DoesNotExist) as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)

    # Return a list of courses
    @action(methods=['GET'], detail=False, url_path='list-courses', name='list all courses',
        authentication_classes=[SessionAuthentication, BasicAuthentication],
        permission_classes=[permissions.IsAuthenticated])
    def list_courses(self, request):
        """
        Returns a list of courses

        Depending on the account type, it returns different set of courses
        """
        try:
            start = request.GET.get('school_start', None)
            end = request.GET.get('school_end', None)

            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            # only board member can see all course.
            if not start or not end or matched_member.member_type != 'B':
                start, end = calender_utils.find_current_school_year()                
            courses = Course.objects.filter(course_status='A',
                                            school_year_start=start,
                                            school_year_end=end)
            courses_json = []
            # extract enrollment
            for c in courses:
                # should only show course that is taught by the teacher
                # TODO(lu): For eacher, they should only be able to see roster and teacher information for active course.
                if matched_member.member_type in ('T', 'V') and not self.__course_taught_by_teacher__(matched_member, c):
                    continue
                course_data = CourseSerializer(c).data
                course_data['enrollment'] = c.students.count()
                instructors = c.instructor
                if instructors:
                    teachers = []
                    for teacher in instructors.all():
                        teachers.append(teacher.user_id.last_name + ' ' + teacher.user_id.first_name)
                    course_data['teacher'] = ','.join(teachers)
                courses_json.append(JSONRenderer().render(course_data))
            content = {
                'courses': courses_json
            }
            return Response(content, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)  

    # Add or update existing course
    @action(methods=['PUT'], detail=False, url_path='upsert-course', name='Add or update a course',
        authentication_classes=[SessionAuthentication, BasicAuthentication],
        permission_classes=[permissions.IsAuthenticated])
    def upsert_course(self, request):
        try:
            course_serializer = CourseSerializer(data=request.data)
            if not course_serializer.is_valid():
                return self.__generate_unsuccessful_response(
                    "Invalid course information is provided", status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user.id)
            if matched_member.member_type != 'B':
                return self.__generate_unsuccessful_response(
                    "The user has no rights to add course!", status.HTTP_401_UNAUTHORIZED)
            matched_course = Course.objects.filter(name=course_serializer.validated_data['name'])
            if matched_course:
                if len(matched_course) > 1:
                    return self.__generate_unsuccessful_response(
                        "There are multiple courses with the same name", status.HTTP_500_INTERNAL_SERVER_ERROR)
            # Can only update class size limit, cost, course_status
                if 'size_limit' in course_serializer.validated_data:
                    matched_course[0].size_limit = course_serializer.validated_data['size_limit']
                if 'course_status' in course_serializer.validated_data:
                    matched_course[0].course_status = course_serializer.validated_data['course_status']
                if 'cost' in course_serializer.validated_data:
                    matched_course[0].cost = course_serializer.validated_data['cost']
                if 'course_description' in course_serializer.validated_data:
                    matched_course[0].course_description = course_serializer.validated_data['course_description']
                matched_course[0].last_update_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
                matched_course[0].last_update_person = user.username
                matched_course[0].save()
                if matched_course[0].size_limit > matched_course[0].students.count():
                    self.__update_waiting_list__(matched_course[0])
                return Response(status=status.HTTP_202_ACCEPTED)
            course = course_serializer.create(course_serializer.validated_data,
                                              username=user.username, member=user.username)
            course.save()
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)  

    @action(methods=['PUT'], detail=False, url_path='delete-course', name='Delete a course',
    authentication_classes=[SessionAuthentication, BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated])
    def remove_course(self, request):
        try:
            course_serializer = CourseSerializer(request.data)
            if not course_serializer.is_valid():
                return self.__generate_unsuccessful_response(
                    "Invalid course information is provided", status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user.id)
            if matched_member.member_type != 'B':
                return self.__generate_unsuccessful_response(
                    "The user has no rights to delete course!", status.HTTP_401_UNAUTHORIZED)
            matched_course = Course.objects.filter(name=course_serializer.validated_data['name'])
            for c in matched_course:
                c.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)     
        

    @action(methods=['GET'], detail=True, url_path='coupon-details', name='get details of a coupon',
    authentication_classes=[SessionAuthentication, BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated])
    def coupon_details(self, request, pk=None):  
        try:
            matched_coupon = self.__fetch_coupon__(request.user, pk)
            return Response(JSONRenderer().render(CouponSerializer(matched_coupon).data),
                            status=status.HTTP_200_OK)
        except ValueError as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)
        except (Coupon.DoesNotExist) as e:
            return self.__generate_unsuccessful_response("The coupon does not exist!", status.HTTP_404_NOT_FOUND)
        
    @action(methods=['GET'], detail=False, url_path='fetch-calendar', name='get calendar',
    authentication_classes=[SessionAuthentication, BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated])
    def get_calendar(self, request):  
        try:
            start_year, end_year = calender_utils.find_current_school_year()
            school_dates = SchoolCalendar.objects.filter(school_year_start = start_year,
                                                         school_year_end = end_year)
            # check if the next year's calendar is available
            next_year_dates = SchoolCalendar.objects.filter(school_year_start = start_year + 1,
                                                            school_year_end = end_year + 1)
            data = []
            for day in school_dates.all():
                data.append(JSONRenderer().render(SchoolCalendarSerializer(day).data))
            for day in next_year_dates.all():
                data.append(JSONRenderer().render(SchoolCalendarSerializer(day).data))
            content = {
                'calendar': data
            }
            return Response(content, status=status.HTTP_200_OK)
        except ValueError as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)
        except SchoolCalendar.DoesNotExist as e:
            return self.__generate_unsuccessful_response("Could not find valid !", status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path='fetch-payments', name='get payments for this or next school year',
    authentication_classes=[SessionAuthentication, BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated])   
    def get_payments(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            payments = Payment.objects.filter(user=matched_member)
            
            start_year, end_year = calender_utils.find_current_school_year()
            next_year_start = start_year + 1
            serialized_payments = []
            for payment in payments.all():
                if payment.registration_code and payment.registration_code.school_year_start.year in (start_year, next_year_start):
                    serialized_payments.append(JSONRenderer().render(PaymentSerializer(payment).data))
            content = {
                'payments': serialized_payments
            }
            return Response(content, status=status.HTTP_200_OK)
        except ValueError as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)
        except SchoolCalendar.DoesNotExist as e:
            return self.__generate_unsuccessful_response("Could not find valid !", status.HTTP_404_NOT_FOUND)
            

    @action(methods=['PUT'], detail=False, url_path='send-notification', name='Send notification to a group',
    authentication_classes=[SessionAuthentication, BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated])   
    def send_notification(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            if matched_member.member_type not in ('B', 'T'):
                raise PermissionError("No notification functionality can be found!")
            if 'message' not in request.data:
                raise ValidationError("No message is provided in the notification request!")
            NotificationUtils.notify(user, request.data['message'])
            return Response(status=status.HTTP_202_ACCEPTED)
        except ValueError as e:
            return self.__generate_unsuccessful_response(str(e), status.HTTP_400_BAD_REQUEST)
        except (PermissionError, User.DoesNotExist, Member.DoesNotExist) as e:
            # convert permission error to NOT_FOUND
            return self.__generate_unsuccessful_response(str(e), status.HTTP_404_NOT_FOUND)
        
    @action(methods=['PUT'], detail=False, url_path='batch-add-teachers',
            name='Create teachers accounts from the provided data',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def AddTeacher(self, request):
        """
         The request should contain a list of teacher's information:
         1. name: in the format of first name + ' ' + last name
         2. email
         3. phone_number
         4. course_name
         5. school_year [optional]. Default to current year if not provided.
        """
        teachers = request.data['teachers']
        for teacher in teachers:
            if not teacher['email']:
                continue
            name = teacher['name'].split()
            if len(name) != 2:
                continue
            try:
                print('adding: ', teacher)
                user = User.objects.get(username=teacher['email'])
                print(user.email, user.date_joined)
                # only create a teacher's account if it does not exist
                member = Member.objects.get(user_id=user)                    
            except User.DoesNotExist as e:
                user_info = {
                        'username': teacher['email'],
                        'first_name': name[0],
                        'last_name': name[1],
                        'email': teacher['email'],
                        'password': 'Sbccl@2024'
                }
                serialized = UserSerializer(data=user_info)
                if not serialized.is_valid():
                    print("invalid user data provided: ", user_info)
                    continue
                user = serialized.create(serialized.validated_data)
                user.save()
                member = Member.objects.create(
                    user_id=user,
                    sign_up_status='V',
                    verification_code='created',
                    member_type='T')
                member.phone_number = teacher['phone_number']
                member.save()
            except Member.DoesNotExist as e:
                member = Member.objects.create(
                    user_id=user,
                    sign_up_status='V',
                    verification_code='created',
                    member_type='T')
                member.phone_number = teacher['phone_number']
                member.save()

                print('member created: ', member)

            if 'class' in teacher:
                start, end = calender_utils.find_current_school_year()
                if 'school_year' in teacher:
                    start, end = teacher['schoo_year'].split('-')
                courses = Course.objects.filter(name=teacher['class'], school_year_start=start,
                                                school_year_end=end)
                print(courses, start, end)
                for c in courses:
                    if 'classroom' in teacher and c.classroom != teacher['classroom']:
                        c.classroom = teacher['classroom']
                        c.save()
                    instructor = InstructorAssignment.objects.filter(course=c, instructor=member)
                    if not instructor:
                        instructor = InstructorAssignment()
                        instructor.course = c
                        instructor.instructor = member
                        instructor.expiration_date = datetime.datetime(end, 7, 1)
                        instructor.school_year_start = datetime.datetime(start, 9, 1)
                        instructor.school_year_end = datetime.datetime(end, 6, 28)
                        instructor.assigned_date = datetime.datetime.today()
                        instructor.last_update_date = datetime.datetime.today()
                        instructor.last_update_person = 'Lu Zhao'
                        instructor.save()

        return Response(status=status.HTTP_201_CREATED)


    @action(methods=['PUT'], detail=False, url_path='batch-add-registrations', name='Send notification to a group',
    authentication_classes=[SessionAuthentication, BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated])
    def batch_add_registrations(self, request):
        """
         The request should contain a list of registration information:
         1. email
         2. per student registrations
        """
        registrations = request.data['registrations']
        print("Adding registrations: ", len(registrations))
        total_added_registration = 0
        total_added_member = 0
        total_added_student = 0
        total_added_language_registration = 0
        total_updated_member = 0
        start, end = calender_utils.find_current_school_year()
        current = 1
        for per_account_reg in registrations:
            print(current)
            current += 1
            print(per_account_reg['email'])
            try:
                if not 'email' in per_account_reg:
                    print("skip missing email entry")
                    continue
                email = per_account_reg['email']
                user = User.objects.filter(username=email)
                if not user:
                    user_info = {
                            'username': email,
                            'first_name': "xx",
                            'last_name': "xx",
                            'email': email,
                            'password': 'Sbccl@2024'
                    }
                    serialized = UserSerializer(data=user_info)
                    if not serialized.is_valid():
                        print("invalid user data provided: ", user_info)
                        continue
                    user = serialized.create(serialized.validated_data)
                    user.save()
                    total_added_member += 1
                    member = Member.objects.create(
                        user_id=user,
                        sign_up_status='V',
                        verification_code='created',
                        member_type='P')
                    member.phone_number = ""
                    member.save()
                    total_added_member += 1
                else:
                    user = user[0]
                    if 'father' in per_account_reg['registrations'][0] and per_account_reg['registrations'][0]['father']:
                        names = per_account_reg['registrations'][0]['father'].split()
                        user.first_name, user.last_name = names[0], names[-1]
                    elif 'mother' in per_account_reg['registrations'][0] and per_account_reg['registrations'][0]['mother']:
                        names = per_account_reg['registrations'][0]['mother'].split()
                        user.first_name, user.last_name = names[0], names[-1]                    
                    user.save()
                    # only create a teacher's account if it does not exist
                    member = Member.objects.get(user_id=user)
                    if 'phone' in per_account_reg['registrations'][0]:
                        member.phone_number = per_account_reg['registrations'][0]['phone']
                    member.save()
                    total_updated_member += 1
                per_student_registration = {}                   
                for registration in per_account_reg['registrations']:
                    if registration['email'].lower() != email.lower():
                        continue

                    student_name = registration['student']
                    if student_name in per_student_registration:
                        per_student_registration[student_name].append(registration)
                    else:
                        per_student_registration[student_name] = [registration]
                for student_name, regs in per_student_registration.items():
                    try:
                        first_name, last_name = student_name.split()
                        student = Student.objects.filter(parent_id=member,
                                                         first_name=first_name,
                                                         last_name=last_name)
                        if not student:
                            date_join = datetime.datetime.today()
                            for r in regs:
                                if 'registration_date' in r and r['registration_date'].strip() != '':
                                    date_join = min(date_join, datetime.datetime.strptime(r['registration_date'], '%Y-%m-%d'))
                            
                            student = {
                                'parent_id': member,
                                'first_name': first_name,
                                'last_name': last_name,
                                'gender': 'U',
                                'date_of_birth': '2019-12-01',
                                # 'chinese_name': 'xxx',
                                'joined_date': '2024-06-11',
                                # 'middle_name': ''
                            }
                            serializer = StudentSerializer(data=student)
                            if not serializer.is_valid():
                                print('Student invalid!', student)
                                return self.__generate_unsuccessful_response(
                                    "Failed to serialize student: {student}".format(student),
                                                        status.HTTP_400_BAD_REQUEST)
                            student = serializer.create(serializer.validated_data)
                            student.parent_id = member
                            student.save()
                            total_added_student += 1
                        else:
                            student = student[0]
                        for r in regs:
                            try:
                                course = Course.objects.filter(name=r['class'])
                                if not course:
                                    return self.__generate_unsuccessful_response(
                                        "No class is found: {class}".format(name=r['class']),
                                        status.HTTP_400_BAD_REQUEST)
                                    continue
                                course = course[0]
                                persist_reg = Registration.objects.filter(student=student,
                                                                          course=course)
                                # find used coupon.
                                #####
                                if not persist_reg:
                                    reg_data = Registration.objects.create(
                                        registration_code = 'xxx-xxx' if not 'registration_code' in r else r['registration_code'],
                                        last_update_date = datetime.datetime.today(),
                                        registration_date = datetime.datetime.today() if 'registration_date' not in r else r['registration_date'],
                                        on_waiting_list = ('status' in r and r['status'] != 'Enrolled'),
                                        student = student,
                                        course = course,
                                        textbook_ordered = ('book_order' in r and r['book_order'] == 'Ordered'),
                                        expiration_date = datetime.date(end, 7, 1),
                                        school_year_start = datetime.date(start, 9, 1),
                                        school_year_end = datetime.date(end, 7, 1)
                                    )
                                    reg_data.save()
                                    total_added_registration += 1
                                else:
                                    reg_data= persist_reg[0]
                                    changed = False
                                    if 'age' in r:
                                        if r['age']:
                                            changed = True
                                            student.date_of_birth = datetime.date(datetime.datetime.today().year - int(r['age']), 12, 1)
                                        else:
                                            student.date_of_birth = datetime.date(2018, 12, 1)
                                    if 'chinese_name' in r and r['chinese_name'].strip():
                                            changed = True
                                            student.chinese_name = r['chinese_name'].strip()
                                    if 'gender' in r and r['gender'].strip():
                                        changed = True
                                        if r['gender'].strip().lower() == 'female':
                                            student.gender = 'F'
                                        elif r['gender'].strip().lower() == 'male':
                                            student.gender = 'M'
                                    if changed:
                                        student.save()    
                                if not 'balance' in r:
                                    total_added_language_registration += 1
                                    continue
                                balance = int(r['balance'])
                                # It's a language registration. 
                                if balance > 0:
                                    total_added_language_registration += 1
                                    if not 'book_order' in r:
                                        continue
                                    book_order = (r['book_order'] == 'Ordered')
                                    original_cost = course.cost + (course.book_cost if book_order else 0)
                                    # Coupon is applied
                                    if original_cost > balance:
                                        coupon = Coupon.objects.filter(dollar_amount=original_cost - balance)
                                        if not coupon:
                                            print("Could not find a coupon for the registration!")
                                        else:
                                            self.__record_coupon_usage__(coupon[0], reg_data, member,
                                                                        datetime.datetime.today if 'registration_date' not in r else r['registration_date'])
                                    # Create payment.
                                    self.__set_up_payment__(reg_data, member,
                                                            datetime.datetime.today if 'registration_date' not in r else r['registration_date'])
                            except Exception as e:
                                return self.__generate_unsuccessful_response(
                                    str(e) + ' for registration: ' + str(r), status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return self.__generate_unsuccessful_response(
                            str(e) + " " + student_name, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return self.__generate_unsuccessful_response(
                            str(e) + " " + student_name, status=status.HTTP_400_BAD_REQUEST)
        msg = 'Total added members: {member}. total updated member {updated_member}. Total added students: {student}. Total added registration: {registrations}. Total added language: {language}'.format(
            member = total_added_member,
            updated_member = total_updated_member,
            student = total_added_student,
            registrations = total_added_registration,
            language = total_added_language_registration
        )
        content = {
            'message': msg
        }
        return Response(content, status=status.HTTP_201_CREATED)
    
    @action(methods=['PUT'], detail=False, url_path='batch-update-students',
        name='Update student information',
        authentication_classes=[SessionAuthentication, BasicAuthentication],
        permission_classes=[permissions.IsAuthenticated])
    def BatchUpdateStudents(self, request):
        if not 'students' in request.data:
            self.__generate_unsuccessful_response(
                "No students are found in the payload", status=status.HTTP_400_BAD_REQUEST)
        not_found_students = 0
        duplicated_student = 0
        num_invalid_rows = 0
        updated_students = 0
        total_processed_payments = len(request.data['students'])
        for s in request.data['students']:
            name_parts = s['student_name'].split()
            if len(name_parts) != 2:
                num_invalid_rows += 1
                continue
            first_name = name_parts[0]
            last_name = name_parts[1]
            if not 'date_of_birth' in s or not s['date_of_birth']:
                num_invalid_rows += 1
                continue
            date_of_birth = datetime.datetime.strptime(s['date_of_birth'], '%m/%d/%Y').date()
            if not 'gender' in s:
                num_invalid_rows += 1
                continue
            gender = 'M'
            if s['gender'].lower() in ('male', 'M'):
                gender = 'M'
            else:
                gender = 'F'
            persisted_student = Student.objects.filter(last_name__iexact = last_name,
                                                       first_name__iexact = first_name,
                                                       gender__iexact = gender)
            if not persisted_student:
                not_found_students + 1
                continue
            if len(persisted_student) > 1:
                duplicated_student += 1
                continue
            total_processed_student += 1
            changed = False
            if persisted_student[0].date_of_birth != date_of_birth:    
                changed = True
                persisted_student[0].date_of_birth = date_of_birth
            if 'chinese_name' in s and s['chinese_name'].strip():
                changed = True
                persisted_student[0].chinese_name = s['chinese_name'].strip()
            if changed:
                persisted_student[0].save()
                updated_students += 1
        msg ='Total processed student: {total}. \n Duplicated_student: {duplicated_student}. \n Not found student: {not_found}. \n Updated student: {updated}'.format(
                total = total_processed_student,
                duplicated_student = duplicated_student,
                not_found = not_found_students,
                updated = updated_students
            )
        return Response(msg, status=status.HTTP_202_ACCEPTED)

    @action(methods=['PUT'], detail=False, url_path='batch-add-payments',
            name='Add payments records for existing registrations',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def AddPayments(self, request):
        if not request.data:
            self.__generate_unsuccessful_response("No payments are found in the payload",
                                                  status=status.HTTP_400_BAD_REQUEST)
        missing_registration = 0
        duplicated_registration = 0
        num_invalid_rows = 0
        invalid_payment = 0
        updated_payment = 0
        inactive_registration = 0
        total_processed_student = len(request.data)
        for payment in request.data:
            if 'status' in payment and payment['status'].lower() == 'inactive':
                inactive_registration += 1
                continue
            name_parts = payment['student_name'].split()
            if len(name_parts) != 2:
                num_invalid_rows += 1
                continue
            first_name = name_parts[0]
            last_name = name_parts[1]
            if not 'class' in payment or not 'tuition_payment' in payment:
                num_invalid_rows += 1
                continue               
            gender = 'M'
            if payment['gender'].lower() in ('male', 'M'):
                gender = 'M'
            else:
                gender = 'F'
            registration = Registration.objects.filter(
                course__name = payment['class'],
                student__first_name__iexact = first_name,
                student__last_name__iexact = last_name,
                student__gender = gender,
                course__course_type = 'L'
            )
            if not registration:
                missing_registration += 1
                continue

            if len(registration) > 1:
                print(registration)
                duplicated_registration += 1
                continue

            persisted_payment = Payment.objects.filter(registration_code_id = registration[0])
            # Update payment.
            if not persisted_payment or len(persisted_payment) > 1:
                invalid_payment += 1
                continue
            if not 'tuition_payment' in payment or not payment['tuition_payment'].isnumeric():
                continue
            persisted_payment[0].amount_in_dollar = float(payment['tuition_payment'])
            persisted_payment[0].pay_date = datetime.datetime.today()
            persisted_payment[0].last_udpate_date = datetime.datetime.today()
            if persisted_payment[0].original_amount > persisted_payment[0].amount_in_dollar:
                persisted_payment[0].payment_status = 'PP'
            else:
                persisted_payment[0].payment_status = 'FP'
            persisted_payment[0].payment_method = 'EL'
            persisted_payment[0].save()
            updated_payment += 1

        msg ='Total processed payment: {total}. \n Invalid rows: {invalid_rows}. Inactive registration {inactive},\n Missing registration: {missing} \nDuplicated_registration: {duplicated}. \n Invalid payment: {invalid_payment}. \n Updated payment: {updated}'.format(
                total = total_processed_student,
                inactive = inactive_registration,
                invalid_rows = num_invalid_rows,
                missing = missing_registration,
                duplicated = duplicated_registration,
                invalid_payment = invalid_payment,
                updated = updated_payment
            )
        return Response(msg, status=status.HTTP_202_ACCEPTED)