# For rest API
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from members import models

# REST APIs
class MemberViewSet(viewsets.ModelViewSet):
    # all members
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, detail=True):
        page = self.paginate_queryset()
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)


    @action(methods=['put'], detail=False)
    def reset_password(self, request, pk=None):
        pass

    @action(methods=['put'], detail=False)
    def login(self, request, pk=None):
        try:
            serialized = UserSerializer(request.user)
            if not serialized.data.is_valid():
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            user = User.objects.get(username=serialized.data.get_username())
            matched_member = models.Member.objects.get(user_id=user.get_username())
            if matched_member.sign_up_status == 'S':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
        except User.DoesNotExist or models.Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def logout(self, request, pk=None):
        try:
            serialized = UserSerializer(request.user)
            if not serialized.is_valid():
                return Response(status=status.HTTP_403_FORBIDDEN)
            user = User.objects.get(serialized.data.get_uername())
            matched_member = models.Member.objects.get(user.get_username())
            if matched_member.sign_up_status == 'S':
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            logout(request, user)
        except User.DoesNotExist or models.Member.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, pk=None):
        print("creating members!")
        if request.user is not None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        content = {
            'user': str(request.user),  # django.contrib.auth.models.AnonyousUser
            'token': str(request.auth)
        }
        serialized = UserSerializer(content['user'])
        if not serialized.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(username=serialized.data.get_username())
        if user is not None:
            return Response(status=status.HTTP_409_CONFLICT)
        
        serialized.data.save()
        print("account created!")
        return Response(status=status.HTTP_201_CREATED)
    
    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    
    def AddStudent(self, request, pk=None):
        pass

    def RemoveStudent(self, request, pk=None):
        pass

    def get_permissions(self):
        return super().get_permissions()