# For rest API
import datetime
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
import pytz
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer, UserSerializer, MemberSerializer, CourseSerializer, RegistrationSerializer
from .models import Course, Member, Student, Registration, Dropout, Payment
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from members import models
import utils.validators.request_validator
import uuid
import json

# REST APIs
class MemberViewSet(ModelViewSet):
    # all members
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def __generate_user_info__(self, user, member):
        balance = self.__calculate_balance__(member)
        return {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number': member.phone_number,
            'member_type': member.getMemberType(),
            'last_login': user.last_login.date(),
            'date_joined': user.date_joined.date(),
            'balance': '{negative}${amount}'.format(negative='-' if balance < 0 else '',
                                                    amount=self.__calculate_balance__(member))
        }

    def __generate_registration_info__(self, registration):
        return json.dumps({
            'student': StudentSerializer(registration.student).data,
            'registration': RegistrationSerializer(registration).data,
            'course': CourseSerializer(registration.course).data})

    def __calculate_balance__(self, member):
        students = Student.objects.filter(parent_id=member)
        balance = 0.0
        for s in students:
            registrations = Registration.objects.filter(student=s)
            for r in registrations:
                balance += r.course.cost
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

    def __send_account_creation_email__(self, new_user, new_member, verification_url):
        user_email_body = "Thanks for registering account in SBCCL school."
        if new_member.member_type != 'P':
            admin_msg = "{email} register a {type} account. Please review this registration!".format(email=new_user.email, type=new_member.getMemberType())
            admin_email_body = admin_msg + "Please click {link} to verify this account.".format(link=verification_url)
            # Email to admin to verify this account.
            send_mail(
                subject="Account registration request",
                message=admin_email_body,
                from_email="no-reply@sbcclny.com",
                # TODO(lu): Remove luzhao@sbcclny.com once the functionality is stable.
                recipient_list=['ccl_admin@sbcclny.com', 'luzhao@sbcclny.com'])
            # Email to user for confirmation.
            user_email_body = user_email_body + """ CCL account admin will review your registration soon. If you have not received any update within a week, please inquery the state by sending email to ccl_board@sbcclny.com."""
        else:
            user_email_body = user_email_body + "Please click {link} to verify this account.".format(link=verification_url)
        new_user.email_user(
            subject="Registration confirmation",
            message=user_email_body)


    def __send_registration_email__(self, user, registration):
        pass

    def __send_unregistration_email__(self, user, dropout):
        pass

    def __update_waiting_list__(self, user, course):
        pass

    def __email_waiting_list_removal__(self, user, registration):
        pass

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
                return Response("This email address has been registered!",
                                status=status.HTTP_409_CONFLICT)
            serialized = UserSerializer(data=request.data)
            if not serialized.is_valid():
                return Response("Invalid data is provided", status=status.HTTP_400_BAD_REQUEST)

            member_type = self.__validate_member_type__(request.data['member_type'])
            if not member_type:
                return Response("Invalid account type is not provided!", status=status.HTTP_400_BAD_REQUEST)

            if 'phone_number' in request.data:
                if not utils.validators.request_validator.ValidatePhoneNumber(request.data['phone_number']):
                    return Response("Invalid phone number is provided",
                                     status=status.HTTP_400_BAD_REQUEST)
                
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
            self.__send_account_creation_email__(new_user, new_member, verification_url)
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
            return Response("Account creation failed: " + str(e), status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['PUT'], detail=False, url_path='login', name='login user',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def login(self, request):
        try:
            matched_member = models.Member.objects.get(user_id=request.user)
            if matched_member.sign_up_status == 'S':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            login(request, request.user)
            user = User.objects.get(username=request.user)
            content = {
                'user': self.__generate_user_info__(user, matched_member),
                'auth': str(request.auth)
            }
            return Response(content, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist: 
            return Response('{username} does not exist'.format(username=request.user.username),
                            status=status.HTTP_404_NOT_FOUND)
        except Member.DoesNotExist:
            return Response('{username} does not exist'.format(username=request.user.username),
                             status=status.HTTP_404_NOT_FOUND)


    @action(methods=['PUT'], detail=True, url_path='logout', name='log out user',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def logout(self, request, pk=None):
        try:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist or models.Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path='account_details', name='Account details',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def account_details(self, request):
        try:
            matched_member = models.Member.objects.get(user_id=request.user)
            if matched_member.sign_up_status == 'S':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(username=request.user)
            content = {
                'user': self.__generate_user_info__(user, matched_member),
                'auth': str(request.auth)
            }
            return Response(content, status=status.HTTP_200_OK)
        except User.DoesNotExist or models.Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
            return Response("No verification code is provided!",status=status.HTTP_400_BAD_REQUEST)
        if email is None:
            return Response("No email was provided!", status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=email)
            matched_members = models.Member.objects.get(user_id=user.id)
            # User has already been verified
            if matched_members.sign_up_status == 'V':
                return Response("The user has already been verified!",
                                status=status.HTTP_409_CONFLICT)
            if matched_members.verification_code != verification_code:
                return Response("Incorrect verification code is provided!",status=status.HTTP_400_BAD_REQUEST)
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
            return Response('There is no user registered with - ' + email,
                             status=status.HTTP_404_NOT_FOUND)
        except Member.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)

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
                return Response("The user does not exist!", status=status.HTTP_404_NOT_FOUND)
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
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("{username} does not exist!".format(username=email_address),
                             status=status.HTTP_404_NOT_FOUND)

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
            return Response('No verification code is provided!', status=status.HTTP_400_BAD_REQUEST)
        new_password = request.query_params.get('password')
        if new_password is None:
            return Response('No password is provided!', status=status.HTTP_400_BAD_REQUEST)
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
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("{email} is not registered".format(email=request.query_params.get('email')),
                            status=status.HTTP_404_NOT_FOUND)

    """
    Reset the password for the user.
    """
    @action(methods=['PUT'], detail=False, url_path='reset-password', name='Reset password.',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def reset_password(self, request, pk=None):
        new_password = request.query_params.get('new_password')
        if new_password is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            validated_pass = UserSerializer().validate_password(new_password)
            user = User.objects.get(username=request.user.username)
            user.password = validated_pass
            user.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        
    @action(methods=['PUT'], detail=False, url_path='add-student', name='Add student to the member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def add_student(self, request):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(JSONRenderer().render(serializer.errors),
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            # Only parent can add students.
            if matched_member.member_type != 'P':
                return Response("Only parent can add students!",
                                status=status.HTTP_400_BAD_REQUEST)
            new_student = serializer.create(serializer.validated_data)
            existing_students = Student.objects.filter(parent_id=matched_member)
            for s in existing_students:
                if s.first_name.upper() == new_student.first_name.upper() and s.last_name.upper() == new_student.last_name.upper():
                    return Response("The student already exists!", status=status.HTTP_409_CONFLICT)
            new_student.parent_id = matched_member
            new_student.save()
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


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
                return Response("Only parent can remove students!",
                                status=status.HTTP_400_BAD_REQUEST)
            existing_students = Student.objects.filter(parent_id=matched_member,
                                                       first_name=student_to_delete.first_name,
                                                       last_name=student_to_delete.last_name)
            if not existing_students:
                return Response("The student does not exist!", status=status.HTTP_400_BAD_REQUEST)
            for s in existing_students:
                registration = Registration.objects.filter(student=s)
                if registration:
                    return Response("""The student still has active enrollments! Please remove their enrollments first on the registration page before removing the student!""",
                                    status=status.HTTP_400_BAD_REQUEST)
                s.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False, url_path='fetch-students',
            name='Get all students for the member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def fetch_students(self, request, pk=None):
        try:
            user = User.objects.get(username=request.user)
            matched_members = models.Member.objects.get(user_id=user)
            students = models.Student.objects.filter(parent_id=matched_members)
            content = {
                'students': [JSONRenderer().render(StudentSerializer(s).data) for s in students]
            }
            return Response(data=content, status=status.HTTP_200_OK)
        except User.DoesNotExist or Member.DoesNotExist:
            return Response('There is no user registered with - ' + request.user,
                             status=status.HTTP_404_NOT_FOUND)

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
            students = models.Student.objects.filter(parent_id=matched_members)
            registrations = []
            dropouts = []
            for s in students:
                matched_registrations = Registration.objects.filter(student=s)
                registrations = registrations + [self.__generate_registration_info__(r) for r in matched_registrations]
                matched_dropouts = Dropout.objects.filter(student=s)
                dropouts = dropouts + [JSONRenderer().render(d) for d in matched_dropouts]
            content = {
                'registrations': registrations,
                'dropouts': dropouts
            }
            return Response(data=content, status=status.HTTP_200_OK)
        except User.DoesNotExist or Member.DoesNotExist:
            return Response('There is no user registered with - ' + request.user,
                             status=status.HTTP_404_NOT_FOUND)

    @action(methods=['PUT'], detail=False, url_path='register-course', name='Register a student to a course',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def register_course(self, request):
        try:
            course_id = request.data['course_id']
            if not course_id:
                return Response("No course is provided", status=status.HTTP_400_BAD_REQUEST)
            persisted_course = Course.objects.get(id=course_id)
            if persisted_course.course_status != 'A':
                return Response("The class is no longer open for registration",
                                status=status.HTTP_400_BAD_REQUEST)
            
            student_serializer = StudentSerializer(data=request.data['student'])
            if not student_serializer.is_valid():
                return Response("Invalid student is provided", status=status.HTTP_400_BAD_REQUEST)
            validated = student_serializer.validated_data

            user = User.objects.get(username=request.user)
            matched_members = models.Member.objects.get(user_id=user)
            persisted_student = Student.objects.get(first_name=validated['first_name'],
                                                    last_name=validated['last_name'],
                                                    parent_id=matched_members)
            matched_registration = Registration.objects.filter(student=persisted_student)
            for m in matched_registration:
                if m.course.course_type == persisted_course.course_type and m.course.course_status == 'A':
                    return Response("The student already registered a same type of course!",
                                    status=status.HTTP_409_CONFLICT)
            registration = Registration()
            registration.registration_code = str(uuid.uuid5(uuid.NAMESPACE_OID,
                                                            persisted_student.first_name + persisted_student.last_name + persisted_course.name))
            registration.on_waiting_list = persisted_course.size_limit <= persisted_course.students.count()
            
            registration.course = persisted_course
            registration.student = persisted_student
            school_year_start = '{year}-{month}-{day}'.format(year=persisted_course.creation_date.year,
                                                              month='09', day='01')
            registration.school_year_start = datetime.datetime.strptime(school_year_start, "%Y-%m-%d")
            registration.school_year_end = registration.school_year_start.replace(year=datetime.datetime.today().year + 1,
                                                                                  month=7)
            registration.registration_date = datetime.datetime.today()
            registration.last_update_date = registration.registration_date
            registration.save()
            self.__send_registration_email__(user, registration)
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist or Member.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist as e:
            return Response(str(3), status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['PUT'], detail=False, url_path='update-registration', name='Update a registration',
        authentication_classes=[SessionAuthentication, BasicAuthentication],
        permission_classes=[permissions.IsAuthenticated])
    def update_registration(self, request):
        try:
            registration_serializer = RegistrationSerializer(data=request.data)
            if not registration_serializer.is_valid():
                return Response("Received invalid registration object!",
                                status=status.HTTP_400_BAD_REQUEST)
            registraion_id = int(request.data['id'])
            matched_registration = Registration.objects.get(id = registraion_id)
            new_course_id = int(request.data['course'])
            if not new_course_id:
                return Response("No course is provided", status=status.HTTP_400_BAD_REQUEST)
            
            # No-op
            if matched_registration.course.id == new_course_id:
                return Response(status=status.HTTP_202_ACCEPTED)
            
            new_course = Course.objects.get(id=new_course_id)
            if new_course.course_status != 'A':
                return Response("The selected class ({name}) is no longer open for registration".format(name=new_course.name),
                                status=status.HTTP_400_BAD_REQUEST)
            # Registration can only be updated for the same type of class.     
            if new_course.course_type != matched_registration.course.course_type:
                return Response(
                    "The registration is for {old_type} class. If you're interested in {new_type} class, please submit a new registration!".format(
                    old_type=matched_registration.course.course_type, new_type=new_course.type),
                    status=status.HTTP_400_BAD_REQUEST)
            old_course = matched_registration.course
            matched_registration.course = new_course
            matched_registration.last_update_date = datetime.datetime.today()
            matched_registration.save()
            user = User.objects.get(username=request.user)
            self.__update_waiting_list__(user, old_course)
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist or Member.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Course.DoesNotExist as e:
            return Response(str(3), status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['PUT'], detail=True, url_path='unregister-course', name='Unregister a student to a course',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def unregister_course(self, request, pk=None):
        try:
            matched_registration = Registration.objects.get(id=pk)
            user = User.objects.get(username=request.user)
            persited_member = Member.objects.get(user_id=user)
            persisted_payment = Payment.objects.filter(registration_code=matched_registration)
            if persisted_payment:
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
                if len(persisted_payment) > 1:
                    return Response("There are more than one payments associated with this registration!",
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                persisted_payment[0].dropout_info = dropout
                persisted_payment[0].last_udpate_date = dropout.dropout_date
                persisted_payment[0].last_update_person = user.username
                persisted_payment[0].save()
                self.__send_unregistration_email__(user, dropout)
            matched_registration.delete()
            self.__update_waiting_list__(user, matched_registration.course)
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist or Member.DoesNotExist:
            return Response('There is no user registered with - ' + request.user,
                             status=status.HTTP_404_NOT_FOUND)
        except Student.DoesNotExist or Course.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except Registration.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)   

    # Return a list of courses
    @action(methods=['GET'], detail=False, url_path='list-courses', name='list all courses',
        authentication_classes=[SessionAuthentication, BasicAuthentication],
        permission_classes=[permissions.IsAuthenticated])
    def list_courses(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            # only board member can see all course.
            show_inactive_class = matched_member.member_type == 'B'
            courses = Course.objects.all()
            courses_json = []
            # extract enrollment
            for c in courses:
                if c.course_status == 'U' and not show_inactive_class:
                    continue
                course_data = CourseSerializer(c).data
                course_data['enrollment'] = len(c.students.all())
                courses_json.append(JSONRenderer().render(course_data))
            content = {
                'courses': courses_json
            }
            return Response(content, status=status.HTTP_200_OK)
        except User.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)  

    # Add or update existing course
    @action(methods=['PUT'], detail=False, url_path='upsert-course', name='Add or update a course',
        authentication_classes=[SessionAuthentication, BasicAuthentication],
        permission_classes=[permissions.IsAuthenticated])
    def upsert_course(self, request):
        try:
            course_serializer = CourseSerializer(data=request.data)
            if not course_serializer.is_valid():
                return Response("Invalid course information is provided",
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user.id)
            if matched_member.member_type != 'B':
                return Response("The user has no rights to add course!",
                                status=status.HTTP_401_UNAUTHORIZED)
            matched_course = Course.objects.filter(name=course_serializer.validated_data['name'])
            if matched_course:
                if len(matched_course) > 1:
                    return Response("There are multiple courses with the same name",
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
                    self.__update_waiting_list__(user, matched_course[0])
                return Response(status=status.HTTP_202_ACCEPTED)
            course = course_serializer.create(course_serializer.validated_data,
                                              username=user.username, member=user.username)
            course.save()
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)  

    @action(methods=['PUT'], detail=False, url_path='delete-course', name='Delete a course',
    authentication_classes=[SessionAuthentication, BasicAuthentication],
    permission_classes=[permissions.IsAuthenticated])
    def remove_course(self, request):
        try:
            course_serializer = CourseSerializer(request.data)
            if not course_serializer.is_valid():
                return Response("Invalid course information is provided",
                                status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user.id)
            if matched_member.member_type != 'B':
                return Response("The user has no rights to delete course!",
                                status=status.HTTP_401_UNAUTHORIZED)
            matched_course = Course.objects.filter(name=course_serializer.validated_data['name'])
            for c in matched_course:
                c.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist as e:
            return Response(str(e), status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)     