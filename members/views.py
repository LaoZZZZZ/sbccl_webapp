# For rest API
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, MemberSerializer
from .models import Member
from .permission_policies import MemberPermissions, IsStaff
# from .authentication_policies import MemberAuthentication
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from members import models
import uuid

# REST APIs
class MemberViewSet(ModelViewSet):
    # all members
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serialized = UserSerializer(data=request.data)
        if not serialized.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={
                                'message':'Invalid data is provided!'
                            })
        new_user = serialized.create(serialized.validated_data)
        print(new_user.username, new_user.password, new_user.email, new_user.last_name,
              new_user.first_name)
        matched_users = User.objects.filter(email=new_user.email)
        if matched_users:
            return Response(status=status.HTTP_409_CONFLICT,
                            data={
                                'message': 'The email already registered'
                            })
        registration_code = str(uuid.uuid5(uuid.NAMESPACE_URL, new_user.username))
        
        new_user.save()
        new_member = Member.objects.create(
            user_id=new_user,
            sign_up_status='S',
            verification_code=registration_code,
            member_type='P') # parent
        
        # TODO(lu): Send confirmation email to the user before saving the user account.
        # new_user.email_user("account created successfully", "Congratulations!")
        new_member.save()
        content = {
            'user': serialized.validated_data,
            'auth': None,
            'verification_url': 'rest_api/members/{username}/verify-user/?verification_code={code}'.format(
                username=new_user.username, code=registration_code)
        }
        return Response(data=content, status=status.HTTP_201_CREATED)

    @action(methods=['PUT'], detail=True, url_path='login', name='login user',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def login(self, request, pk=None):
        try:
            matched_member = models.Member.objects.get(user_id=request.user)
            if matched_member.sign_up_status == 'S':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            login(request, request.user)
            content = {
                'user': str(request.user),
                'auth': str(request.auth)
            }
            return Response(content, status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist: 
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    @action(methods=['PUT'], detail=True, url_path='logout', name='log out user',
            authentication_classes=[SessionAuthentication, BasicAuthentication],
            permission_classes=[permissions.IsAuthenticated])
    def logout(self, request, pk=None):
        try:
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except User.DoesNotExist or models.Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    """
     Verify the signup for the user.
    """
    @action(methods=['PUT'], detail=True, url_path='verify-user', name='Verify the user.',
            authentication_classes=[BasicAuthentication],
            permission_classes=[permissions.AllowAny])
    def verify_user(self, request, pk=None):
        verification_code = request.query_params.get('verification_code')
        if verification_code is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=pk)
            matched_members = models.Member.objects.filter(user_id=user.id,
                                                           verification_code=verification_code)
            if not matched_members:
                return Response(status=status.HTTP_404_NOT_FOUND)
            for m in matched_members:
                m.sign_up_status = 'V'
                m.save()
            return Response(status=status.HTTP_202_ACCEPTED)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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
                m.verification_code = ''
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

        
    # @action(methods=['PUT'], detail=True, url_name='login', name='login user',
    #         authentication_classes=[SessionAuthentication, BasicAuthentication],
    #         permission_classes=[IsOwner | IsStaff])
    # def AddStudent(self, request, pk=None):
    #     pass


    # @action(methods=['PUT'], detail=True, url_name='login', name='login user',
    #         authentication_classes=[SessionAuthentication, BasicAuthentication],
    #         permission_classes=[IsOwner | IsStaff])
    # def RemoveStudent(self, request, pk=None):
    #     pass    