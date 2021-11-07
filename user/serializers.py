from abc import ABC
from seminar.models import Seminar
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import update_last_login
from django.db.models import F

from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from user.models import ParticipantProfile, InstructorProfile

# 토큰 사용을 위한 기본 세팅
User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


# [ user -> jwt_token ] function
def jwt_token_of(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    return jwt_token


class UserCreateSerializer(serializers.Serializer):
    instructor = serializers.SerializerMethodField()
    participant = serializers.SerializerMethodField()

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    role = serializers.CharField(required=True)
    
    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        role = data.get('role')
        if not role or ( role.split(",")[0] not in ['instructor', 'participant'] ):
            raise serializers.ValidationError("role이 지정되지 않았습니다.")
        data.update({'role' : role.replace(" ", "")})
        if bool(first_name) ^ bool(last_name):
            raise serializers.ValidationError("성과 이름 중에 하나만 입력할 수 없습니다.")
        if first_name and last_name and not (first_name.isalpha() and last_name.isalpha()):
            raise serializers.ValidationError("이름에 숫자가 들어갈 수 없습니다.")
        return data

    def create(self, validated_data):
        # TODO (1. 유저 만들고 (ORM) , 2. 비밀번호 설정하기; 아래 코드를 수정해주세요.)
        roles = validated_data['role'].split(",")
        user = User.objects.create_user(**validated_data)

        return user, jwt_token_of(user)


class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("이메일 또는 비밀번호가 잘못되었습니다.")

        update_last_login(None, user)
        return {
            'email': user.email,
            'token': jwt_token_of(user)
        }


class UserSerializer(serializers.ModelSerializer):
    instructor = serializers.SerializerMethodField()
    participant = serializers.SerializerMethodField()

    class Meta:
        model = User
        # Django 기본 User 모델에 존재하는 필드 중 일부
        fields = (
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'last_login',  # 가장 최근 로그인 시점
            'date_joined',  # 가입 시점
            'participant',
            'instructor'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def get_participant(self, user):
        if user.participant:
            return ParticipantProfileSerializer(user.participant, context=self.context).data
        return None

    def get_instructor(self, user):
        if user.instructor:
            return InstructorProfileSerializer(user.instructor, context=self.context).data
        return None

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if bool(first_name) ^ bool(last_name):
            raise serializers.ValidationError("성과 이름 중에 하나만 입력할 수 없습니다.")
        if first_name and last_name and not (first_name.isalpha() and last_name.isalpha()):
            raise serializers.ValidationError("이름에 숫자가 들어갈 수 없습니다.")
        return super().validate(data)
    
    def create(self, validated_data):
        user = super().create(validated_data)
        return user

class UserInstructorSerializer(serializers.Serializer):
    joined_at = serializers.ReadOnlyField(source='userseminar')
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'joined_at'
        )

class UserParticipantSerializer(serializers.Serializer):
    joined_at = serializers.ReadOnlyField(source='userseminar')
    is_active = serializers.ReadOnlyField(source='userseminar')
    dropped_at = serializers.ReadOnlyField(source='userseminar')
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'joined_at',
            'is_active',
            'dropped_at'
        )

class ParticipantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantProfile
        fields = (
            'id',
            'university',
            'accepted'
        )
    def validate(self, data):
        if data.get('accepted', None)== None:
            data.update({'accepted' : True})
        return {
            'university': data.get("university") or "",
            'accepted': data.get("accepted")
        }

    def create(self, validated_data):
        participant = super().create(validated_data)
        return participant

class InstructorProfileSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(min_value=0)
    class Meta:
        model = InstructorProfile
        fields = (
            'id',
            'company',
            'year'
        )

    def validate(self, data):
        return data

    def create(self, validated_data):
        instructor = super().create(validated_data)
        return instructor

class UserWithSeminarSerializer(UserSerializer):

    def get_participant(self, user):
        if user.participant:
            return ParticipantProfileWithSeminarSerializer(user.participant, context=self.context).data
        return None

    def get_instructor(self, user):
        if user.instructor:
            return InstructorProfileWithSeminarSerializer(user.instructor, context=self.context).data
        return None

class ParticipantProfileWithSeminarSerializer(ParticipantProfileSerializer):
    seminars = serializers.SerializerMethodField()
    class Meta(ParticipantProfileSerializer.Meta):
        fields = ParticipantProfileSerializer.Meta.fields \
                + ('seminars',)

    def get_seminars(self, participant):
        queryset = Seminar.objects.filter(userseminar__role='participant',userseminar__user__participant=participant.id)
        response = queryset.annotate(
            joined_at=F('userseminar__joined_at'),
            is_active=F('userseminar__is_active'),
            dropped_at=F('userseminar__dropped_at')
            ).values(
                'id',
                'name',
                'joined_at',
                'is_active',
                'dropped_at'
                )
        return response

class InstructorProfileWithSeminarSerializer(InstructorProfileSerializer):
    charge = serializers.SerializerMethodField()
    class Meta(InstructorProfileSerializer.Meta):
        fields = InstructorProfileSerializer.Meta.fields \
                + ('charge',)

    def get_charge(self, instructor):
        try : queryset = Seminar.objects.get(userseminar__role='instructor',userseminar__user__instructor=instructor.id)
        except : return None
        response = queryset.annotate(
            joined_at=F('userseminar__joined_at')
            ).values(
                'id',
                'name',
                'joined_at'
                )
        return response
