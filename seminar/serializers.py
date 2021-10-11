from rest_framework import serializers, status
from django.core.exceptions import PermissionDenied
from django.db.models import F

from seminar.models import Seminar, UserSeminar
from user.models import User
from user.serializers import UserInstructorSerializer, UserParticipantSerializer
from django.utils.encoding import force_text
from rest_framework import status
from rest_framework.exceptions import APIException

class CustomException(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = ''

    def __init__(self, detail, status_code):
        self.detail = detail
        self.status_code = status_code
        
class SeminarSerializer(serializers.ModelSerializer):
    instructors = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    time = serializers.TimeField(format='%H:%M',input_formats=['%H:%M',])
    online = serializers.BooleanField(default=True)
    capacity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Seminar
        fields = (
            'id',
            'name',
            'capacity',
            'count',
            'time',
            'online',
            'instructors',
            'participants',
        )
        write_only_fields = ('participant_count')

    def get_instructors(self, seminar):
        queryset = User.objects.filter(userseminar__seminar=seminar, userseminar__role='instructor')
        response = queryset.annotate(
            joined_at=F('userseminar__joined_at')
            ).values(
                'id',
                'username',
                'email',
                'first_name',
                'last_name',
                'joined_at'
                )
        return response

    def get_participants(self, seminar):
        queryset = User.objects.filter(userseminar__seminar=seminar, userseminar__role='participant')
        response = queryset.annotate(
            joined_at=F('userseminar__joined_at'),
            is_active=F('userseminar__is_active'),
            dropped_at=F('userseminar__dropped_at')
            ).values(
                'id',
                'username',
                'email',
                'first_name',
                'last_name',
                'joined_at',
                'is_active',
                'dropped_at'
                )
        return response

    def validate(self, data):
        name = data.get('name')
        capacity = data.get('capacity')
        count = data.get('count')
        time = data.get('time') 

        #if capacity and capacity <= 0: raise CustomException("capacity가 양수가 아닙니다.", status.HTTP_400_BAD_REQUEST)
        if self.instance != None:
            parti_count = self.instance.participant_count
            if capacity and capacity < parti_count: 
                raise CustomException("capacity가 현재 참여자 보다 작을 수 없습니다. 현재 인원 : " + str(parti_count) \
                    , status.HTTP_400_BAD_REQUEST)
        if count and count <= 0: raise CustomException("count가 양수가 아닙니다.", status.HTTP_400_BAD_REQUEST)

        return data

    def create(self, validated_data):
        return super().create(validated_data)

class SeminarNameSerializer(SeminarSerializer):
    #participant_count = serializers.SerializerMethodField()
    class Meta:
        model = Seminar
        fields = (
            'id',
            'name',
            'instructors',
            'participant_count'
        )

    #def get_participant_count(self, seminar):
    #    queryset = User.objects.filter(userseminar__seminar=seminar, userseminar__role='participant')
    #    return queryset.count()

class SeminarApplySerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    seminar_id = serializers.IntegerField(required=True)
    role = serializers.CharField(required=True)

    def validate(self, data):
        
        user_id = data.get('user_id', None)
        seminar_id = data.get('seminar_id', None)

        role = data.get('role')
        user = User.objects.get(id=user_id)
        instructing_seminars = UserSeminar.objects.filter(user=user_id, role='instructor')
        try:
            us = UserSeminar.objects.get(seminar=seminar_id, user=user_id)
            if us:
                already_signed = True
                is_active = us.is_active
            else : already_signed = False
        except:
            already_signed = False
        
        if already_signed == True:
            if is_active == False:
                raise CustomException("드랍한 세미나는 다시 참여할 수 없습니다.", status.HTTP_400_BAD_REQUEST)
            raise CustomException("이미 해당 세미나에 참여 중입니다.", status.HTTP_400_BAD_REQUEST)

        if role not in ['participant','instructor'] :
            raise CustomException("role이 잘못되었습니다.", status.HTTP_400_BAD_REQUEST)
        if getattr(user,role) == None:
            raise CustomException(f"{role}의 자격이 없습니다.", status.HTTP_403_FORBIDDEN)
        if role == 'instructor' and instructing_seminars.exists():
            raise CustomException("이미 다른 세미나의 instructor입니다", status.HTTP_400_BAD_REQUEST)
        if role == 'participant' and user.participant.accepted is False :
            raise CustomException("accepted되지 않았습니다.", status.HTTP_403_FORBIDDEN)
        if Seminar.objects.get(id=seminar_id).participant_count >= Seminar.objects.get(id=seminar_id).capacity:
            raise CustomException("세미나 정원이 찼습니다.", status.HTTP_400_BAD_REQUEST)
        
        
        return ""        

class UserSeminarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSeminar
        fields = (
            'user',
            'seminar',
            'role',
            'joined_at',
            'is_active',
            'dropped_at'
        )
    def validate(self, data):
        return data
    def create(self, validated_data):
        return super().create(validated_data)

