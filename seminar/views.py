from datetime import time
from functools import partial
from re import S
from user.serializers import User
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from seminar.serializers import SeminarSerializer, SeminarNameSerializer, SeminarApplySerializer, UserSeminarSerializer
from seminar.models import Seminar, UserSeminar


class SeminarViewSet(viewsets.GenericViewSet):
    queryset = Seminar.objects.all()
    serializer_class = SeminarSerializer
    permission_classes = (permissions.IsAuthenticated(), )

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return (permissions.AllowAny(), )
        return self.permission_classes

    def list(self, request):
        name = self.request.query_params.get('name')
        order = self.request.query_params.get('order')

        if name :
            seminars = Seminar.objects.filter(name__contains=name)
        else :
            seminars = self.get_queryset()

        if order=='earliest' :
            seminars = seminars.order_by('created_at')
        else :
            seminars = seminars.order_by('-created_at')

        return Response(SeminarNameSerializer(seminars, many=True).data)

    # /api/v1/user/seminar/{pk}
    def retrieve(self, request, pk=None):
        try : 
            seminar = Seminar.objects.get(id=pk)
        except :
            return Response(status=status.HTTP_404_NOT_FOUND, data='세미나가 존재하지 않습니다.')

        return Response(self.get_serializer(seminar).data)

    #/api/v1/seminar/{seminar_id}/user/
    @action(methods=['post', 'delete'], detail=True)
    def user(self, request, pk):
        if request.method.lower() == 'post':
            try : 
                seminar = Seminar.objects.get(id=pk)
            except :
                return Response(status=status.HTTP_404_NOT_FOUND, data='세미나가 존재하지 않습니다.')
            data = request.data.copy()
            data.update({'user_id' : request.user.id, 'seminar_id' : pk,})

            serializer = SeminarApplySerializer(seminar, data=data)
            serializer.is_valid(raise_exception=True)

            us_data = {    
                'user' : request.user.id,
                'seminar' : pk,
                'role' : data.get('role'),
                'joined_at' : timezone.now(),
                'is_active' : True
            }
            us_serializer = UserSeminarSerializer(data=us_data)
            us_serializer.is_valid(raise_exception=True)
            us_serializer.save()
            if data.get('role') == 'participant' :
                seminar.participant_count += 1
            seminar.save()
            return Response(self.get_serializer(seminar).data,status=status.HTTP_201_CREATED)

        if request.method.lower() == 'delete':
            try : 
                seminar = Seminar.objects.get(id=pk)
            except :
                return Response(status=status.HTTP_404_NOT_FOUND, data='세미나가 존재하지 않습니다.')

            user_id = request.user.id
            try : 
                userseminar = UserSeminar.objects.get(user=user_id,seminar=pk)
            except :
                return Response(self.get_serializer(seminar).data,status=status.HTTP_200_OK)
            if userseminar.role == 'instructor':
                return Response(status=status.HTTP_403_FORBIDDEN, data='참여자들을 버릴 수 없습니다')

            us_data = {    
                'is_active' : False,
                'dropped_at' : timezone.now()
            }
            us_serializer = UserSeminarSerializer(userseminar, data=us_data, partial=True)
            us_serializer.is_valid(raise_exception=True)
            us_serializer.update(userseminar, us_serializer.validated_data)

            seminar.participant_count -= 1
            seminar.save()
            return Response(self.get_serializer(seminar).data,status=status.HTTP_200_OK)

    def create(self, request):
        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN, data='로그인이 필요합니다.')

        roles = request.user.role.split(",")
        check_ins = False
        for role in roles:
            if role == "instructor":
                check_ins = True
        if check_ins is False :
            return Response(status=status.HTTP_403_FORBIDDEN, data='Instructor가 아닙니다.')

        data = request.data.copy()
        data.update({'user_id' : request.user.id})
        data.update({'participant_count' : 0})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        seminar = serializer.data

        us_data = {    
            'user' : request.user.id,
            'seminar' : seminar['id'],
            'role' : 'instructor',
            'joined_at' : timezone.now,
            'is_active' : True
        }
        us_serializer = UserSeminarSerializer(data=us_data)
        us_serializer.is_valid(raise_exception=True)
        us_serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
    
    def update(self, request, pk):
        user = request.user
        #userSeminar = request.user.userseminar
        userseminar = UserSeminar.objects.get(seminar_id=pk,role='instructor')
        if userseminar.user != user:
            return Response(status=status.HTTP_403_FORBIDDEN, data='Instructor가 아닙니다.')

        serializer = self.get_serializer(userseminar.seminar, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(userseminar.seminar, serializer.validated_data)
        
        return Response(status=status.HTTP_200_OK, data=serializer.data)
