from functools import partial
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db import IntegrityError
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from user.serializers import UserSerializer, UserLoginSerializer, UserCreateSerializer, UserWithSeminarSerializer
from user.serializers import ParticipantProfileSerializer, InstructorProfileSerializer

User = get_user_model()

class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, jwt_token = serializer.save()
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT, data='이미 존재하는 유저 이메일입니다.')

        roles = request.data.get('role').split(",")
        for role in roles:
            if role.strip() == "participant":
                sub_serializer = ParticipantProfileSerializer(data=request.data, partial=True)
                try : 
                    sub_serializer.is_valid(raise_exception=True)
                except Exception as e: 
                    user.delete()
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)
                user.participant = sub_serializer.save()
            if role.strip() == "instructor":
                sub_serializer = InstructorProfileSerializer(data=request.data, partial=True)
                try : 
                    sub_serializer.is_valid(raise_exception=True)
                except Exception as e: 
                    user.delete()
                    return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)
                user.instructor = sub_serializer.save()
        
        user.save()

        return Response({'user': user.email, 'token': jwt_token}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request):

        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.GenericViewSet):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # /api/v1/user/participant/
    @action(methods=['post'], detail=False)
    def participant(self, request):
        user = request.user
        data = request.data.copy()

        if user.participant != None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='이미 참여자입니다.')
        sub_serializer = ParticipantProfileSerializer(data=data, partial=True)
        try : 
            sub_serializer.is_valid(raise_exception=True)
        except Exception as e: 
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)
        user.participant = sub_serializer.save()
        user.save()

        return Response(self.get_serializer(user).data)

    def update(self, request, pk=None):
        if pk != 'me':
            return Response(status=status.HTTP_403_FORBIDDEN, data='다른 유저 정보를 수정할 수 없습니다.')

        user = request.user

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(user, serializer.validated_data)
        try : 
            data_forupdate = request.data.copy()
            data_forupdate.pop('accepted', None)
            if user.participant:
                p_serializer = ParticipantProfileSerializer(user.participant, data=data_forupdate, partial=True)
                p_serializer.is_valid(raise_exception=True)
                p_serializer.update(user.participant, p_serializer.validated_data)
            if user.instructor:
                i_serializer = InstructorProfileSerializer(user.instructor, data=data_forupdate, partial=True)
                i_serializer.is_valid(raise_exception=True)
                i_serializer.update(user.instructor, i_serializer.validated_data)
        except Exception as e: 
            return Response(status=status.HTTP_400_BAD_REQUEST, data=e.detail)      
##
        return Response(status=status.HTTP_200_OK, data='유저 정보가 정상적으로 수정되었습니다.')

    def retrieve(self, request, pk=None):

        if request.user.is_anonymous:
            return Response(status=status.HTTP_403_FORBIDDEN, data='먼저 로그인 하세요.')

        user = request.user if pk == 'me' else self.get_object()
        return Response(UserWithSeminarSerializer(user).data)
