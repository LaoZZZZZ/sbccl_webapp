# For rest API
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer, UserSerializer, MemberSerializer
from .models import Member, Student
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from members import models
import utils.validators.request_validator
import uuid

# REST APIs
class MemberViewSet(ModelViewSet):
    # all members
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def __generate_user_info__(self, user, member):
        return {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_number:': member.phone_number,
            'member_type': member.member_type
        }

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        new_user = None
        try:
            serialized = UserSerializer(data=request.data)
            if not serialized.is_valid():
                return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
            new_user = serialized.create(serialized.validated_data)
            registration_code = str(uuid.uuid5(uuid.NAMESPACE_URL, new_user.username))
            new_user.save()
            new_member = Member.objects.create(
                user_id=new_user,
                sign_up_status='S',
                verification_code=registration_code,
                member_type='P') # parent
            if 'phone_number' in request.data:
                if not utils.validators.request_validator.ValidatePhoneNumber(request.data['phone_number']):
                    return Response("Invalid phone number is provided",
                                     status=status.HTTP_400_BAD_REQUEST)
                new_member.phone_number = request.data['phone_number']
            # TODO(lu): Send confirmation email to the user before saving the user account.
            # new_user.email_user("account created successfully", "Congratulations!")
            new_member.save()
            verification_url = 'http://localhost:8000/rest_api/members/verify-user/?verification_code={code}'.format(
                    code=registration_code)
            msg = "Thanks for registering account in SBCCL school. Please click {link} to verify this account.".format(link=verification_url)
            new_user.email_user(
                subject="Registration confirmation",
                message=msg)
            content = {
                'user': serialized.validated_data,
                'auth': None,
                'verification_url': verification_url
            }
            response = Response(data=content, status=status.HTTP_201_CREATED)
            response['location'] = registration_code
            return response
        except Exception as e:
            # delete the user so that the user can retry.
            if new_user:
                new_user.delete()
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


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
            logout(request.user)
            return Response(status=status.HTTP_200_OK)
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
        if verification_code is None or verification_code == '':
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            matched_members = models.Member.objects.filter(verification_code=verification_code)
            if not matched_members:
                return Response(status=status.HTTP_404_NOT_FOUND)
            verified = False
            for m in matched_members:
                if m.verification_code == verification_code:
                    m.sign_up_status = 'V'
                    m.verification_code = None
                    m.save()
                    verified = True
            if not verified:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response('There is no user having the provided verification code - ' + verification_code,
                             status=status.HTTP_404_NOT_FOUND)

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
    @action(methods=['PUT'], detail=True, url_path='reset-password-by-code',
            name='Verify the user.',
            authentication_classes=[BasicAuthentication],
            permission_classes=[permissions.AllowAny])
    def reset_password_by_code(self, request, pk=None):
        verification_code = request.query_params.get('verification_code')
        if verification_code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        new_password = request.query_params.get('new_password')
        if new_password is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            validated_pass = UserSerializer().validate_password(new_password)
            retrieved_user = User.objects.get(username=pk)
            matched_members = Member.objects.filter(user_id=retrieved_user.id,
                                                    verification_code=verification_code)
            if not matched_members:
                return Response(status=status.HTTP_404_NOT_FOUND)
            retrieved_user.password = validated_pass 
            retrieved_user.save()
            for m in matched_members:
                m.verification_code = None
                m.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
    Reset the password for the user.
    """
    @action(methods=['PUT'], detail=True, url_path='reset-password', name='Reset password.',
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

        
    @action(methods=['PUT'], detail=True, url_path='add-student', name='Add student to the member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def add_student(self, request, pk=None):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            # Only parent can add students.
            if matched_member.member_type != 'P':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            new_student = serializer.create(serializer.validated_data)
            existing_students = Student.objects.filter(parent_id=matched_member)
            for s in existing_students:
                if s.first_name == new_student.first_name and s.last_name == new_student.last_name:
                    return Response(status=status.HTTP_409_CONFLICT)
            new_student.parent_id = matched_member
            new_student.save()
            return Response(status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    @action(methods=['PUT'], detail=True, url_path='remove-student', name='Remove student from member',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def remove_student(self, request, pk=None):
        try:
            serializer = StudentSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            student_to_delete = serializer.create(serializer.validated_data)
            user = User.objects.get(username=request.user.username)
            matched_member = Member.objects.get(user_id=user)
            # Only parent can remove students.
            if matched_member.member_type != 'P':
                return Response(status=status.HTTP_400_BAD_REQUEST)
            existing_students = Student.objects.filter(parent_id=matched_member,
                                                       first_name=student_to_delete.first_name,
                                                       last_name=student_to_delete.last_name)
            for s in existing_students:
                s.delete()
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['PUT'], detail=True, url_path='register-course', name='Register a student to a course',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def register_course(self, request, pk=None):
        pass

    @action(methods=['PUT'], detail=True, url_path='unregister-course', name='Unregister a student to a course',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def unregister_course(self, request, pk=None):
        pass   