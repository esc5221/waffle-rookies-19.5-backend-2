import re
import json
from django.http import request
from factory.django import DjangoModelFactory
from django.db import transaction

from user.models import User
from django.test import TestCase
from django.test import tag
from rest_framework import status
import json

from user.models import InstructorProfile, ParticipantProfile
from user.serializers import jwt_token_of

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = 'test@test.com'

    @classmethod
    def create(cls, **kwargs):
        is_instructor, is_participant = kwargs.pop('is_instructor', False), kwargs.pop('is_participant', False)
        user = User.objects.create(**kwargs)
        user.set_password(kwargs.get('password', ''))
        user.save()
        if is_instructor:
            user.instructor = InstructorProfile.objects.create()
            user.instructor.save()
        if is_participant:
            user.participant = ParticipantProfile.objects.create()
            user.participant.save()
        user.save()
        return user

# POST /api/v1/signup/
class PostUserTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        # 수강생 프로필을 가진 유저 만들기
        # 위 코드의 팩토리 구현을 참고해주세요.
        # UserFactory() 따위로 instance를 만들면,
        # 자동적으로 내부의 classmethod 'create'가 실행됩니다.
        # is_instructor, is_participant 옵션은 제가 임의로 추가한 편의기능입니다.

        cls.user = UserFactory(
            email='waffle@test.com',
            username='steve',
            first_name='지혁',
            last_name='강',
            password='password',
            is_participant=True
        )
        cls.user.participant.university = '서울대학교'
        cls.user.participant.save()

        # 클래스 전반에 걸쳐 기본적으로 사용할 데이터라면, 여기서 선언해줄 수 있습니다.
        # 이러한 개념을 FIXTURE 라고 합니다.
        cls.post_data = {
            'email': 'waffle@test.com',
            'username': 'steve',
            'password': 'password',
            'role': 'participant'
        }

    def test_post_user_중복(self):
        data = self.post_data
        with transaction.atomic():
            response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_post_user_잘못된_request들(self):
        data = self.post_data.copy()
        data.update({'role': 'wrong_role'})
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.post_data.copy()
        data.pop('role')
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = self.post_data.copy()
        data.pop('role')
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_post_user(self):
        data = {
            "username": "participant",
            "password": "password",
            "first_name": "Davin",
            "last_name": "Byeon",
            "email": "bdv111@snu.ac.kr",
            "role": "participant",
            "university": "서울대학교"
        }
        response = self.client.post('/api/v1/signup/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertEqual(data["user"], "bdv111@snu.ac.kr")
        self.assertIn("token", data)

        user_count = User.objects.count()
        self.assertEqual(user_count, 2)
        participant_count = ParticipantProfile.objects.count()
        self.assertEqual(participant_count, 2)
        instructor_count = InstructorProfile.objects.count()
        self.assertEqual(instructor_count, 0)

# PUT /api/v1/user/me/
class PutUserMeTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.participant = UserFactory(
            username='part',
            password='password',
            first_name='Davin',
            last_name='Byeon',
            email='bdv111@snu.ac.kr',
            is_participant=True
        )
        cls.participant.participant.university = '서울대학교'
        cls.participant.save()
        cls.participant_token = 'JWT ' + jwt_token_of(User.objects.get(email='bdv111@snu.ac.kr'))

        cls.instructor = UserFactory(
            username='inst',
            password='password',
            first_name='Davin',
            last_name='Byeon',
            email='bdv123@snu.ac.kr',
            is_instructor=True
        )
        cls.instructor.instructor.year = 1
        cls.instructor.save()
        cls.instructor_token = 'JWT ' + jwt_token_of(User.objects.get(email='bdv123@snu.ac.kr'))

    def test_put_user_incomplete_request(self):
        # No Token

        response = self.client.put('/api/v1/user/me/',
                                   data={"first_name": "Dabin"}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Only First Name
        response = self.client.put('/api/v1/user/me/',
                                   data={"first_name": "Dabin"},
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=self.participant_token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        participant_user = User.objects.get(username='part')
        self.assertEqual(participant_user.first_name, 'Davin')

        # wrong year value
        wrong_year_data = {
            "username": "inst123",
            "company": "매스프레소",
            "year": -1
        }
        response = self.client.put('/api/v1/user/me/',
                                   data=wrong_year_data,
                                   content_type='application/json',
                                   HTTP_AUTHORIZATION=self.instructor_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        instructor_user = User.objects.get(username='inst')
        self.assertEqual(instructor_user.email, 'bdv123@snu.ac.kr')

    def test_put_user_me_participant(self):

        data = {
            "username": "part123",
            "email": "bdv111@naver.com",
            "university": "경북대학교"
        }
        response = self.client.put(
            '/api/v1/user/me/',
            data=data,
            content_type='application/json',
            HTTP_AUTHORIZATION=self.participant_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "part123")
        self.assertEqual(data["email"], "bdv111@naver.com")
        self.assertEqual(data["first_name"], "Davin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertNotIn("token", data)

        participant = data["participant"]
        self.assertIsNotNone(participant)
        self.assertIn("id", participant)
        self.assertEqual(participant["university"], "경북대학교")
        self.assertTrue(participant["accepted"])
        self.assertEqual(len(participant["seminars"]), 0)

        self.assertIsNone(data["instructor"])
        participant_user = User.objects.get(username='part123')
        self.assertEqual(participant_user.email, 'bdv111@naver.com')

    def test_put_user_me_instructor(self):
        response = self.client.put(
            '/api/v1/user/me/',
            data = {
                "username": "inst123",
                "email": "bdv111@naver.com",
                "first_name": "Dabin",
                "last_name": "Byeon",
                "university": "서울대학교",  # this should be ignored
                "company": "매스프레소",
                "year": 2
            },
            content_type='application/json',
            HTTP_AUTHORIZATION=self.instructor_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["username"], "inst123")
        self.assertEqual(data["email"], "bdv111@naver.com")
        self.assertEqual(data["first_name"], "Dabin")
        self.assertEqual(data["last_name"], "Byeon")
        self.assertIn("last_login", data)
        self.assertIn("date_joined", data)
        self.assertNotIn("token", data)

        self.assertIsNone(data["participant"])

        instructor = data["instructor"]
        self.assertIsNotNone(instructor)
        self.assertIn("id", instructor)
        self.assertEqual(instructor["company"], "매스프레소")
        self.assertEqual(instructor["year"], 2)
        #self.assertIsNone(instructor["charge"])

        instructor_user = User.objects.get(username='inst123')
        self.assertEqual(instructor_user.email, 'bdv111@naver.com')

# POST /api/v1/login/
class PostUserLogin(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory(
            username='part',
            password='password',
            first_name='first_1',
            last_name='last_1',
            email='user_1@snu.ac.kr',
            is_participant=True
        )

        cls.post_data = {
            'email': 'user_1@snu.ac.kr',
            'password': 'password'
        }

    def test_post_login(self):
        response = self.client.post('/api/v1/login/', 
                                    content_type='application/json',
                                    data=self.post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['token'], jwt_token_of(User.objects.get(email='user_1@snu.ac.kr')))

# GET /api/v1/user/me/
class GetUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory(
            username='part',
            password='password',
            first_name='first_1',
            last_name='last_1',
            email='user_1@snu.ac.kr',
            is_participant=True
        )
        cls.user_1.participant.university = '서울대학교'
        cls.user_1.participant.save()
        cls.user_1_token = 'JWT ' + jwt_token_of(User.objects.get(email='user_1@snu.ac.kr'))

        cls.user_2 = UserFactory(
            username='inst',
            password='password',
            first_name='first_2',
            last_name='last_2',
            email='user_2@snu.ac.kr',
            is_instructor=True
        )
        cls.user_2_token = 'JWT ' + jwt_token_of(User.objects.get(email='user_2@snu.ac.kr'))
        cls.user_3 = UserFactory(
            username='partinst',
            password='password',
            first_name='first_3',
            last_name='last_3',
            email='user_3@snu.ac.kr',
            is_instructor=True,
            is_participant=True
        )
        cls.user_3_token = 'JWT ' + jwt_token_of(User.objects.get(email='user_3@snu.ac.kr'))
        cls.username_list = ['part', 'inst', 'partinst']

    def test_get_user(self):
        
        for i in range(1,3):
            with transaction.atomic():
                response = self.client.get('/api/v1/user/me/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"user_{i}_token"))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                data = response.json()
                self.assertEqual(data['username'], self.username_list[i-1])
                self.assertEqual(data['email'], f"user_{i}@snu.ac.kr")
                self.assertEqual(data['first_name'], f'first_{i}')
                self.assertEqual(data['last_name'], f'last_{i}')
                self.assertIn("last_login", data)
                self.assertIn("date_joined", data)

# POST /api/v1/user/participant/
class PostUserParticipant(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1,4) : 
            user = UserFactory(
                username=f"inst_{i}",
                password='password',
                first_name='first',
                last_name='last',
                email=f'inst_{i}@snu.ac.kr',
                is_instructor=True
            )
            setattr(cls, f"inst_{i}", user)
            token = 'JWT ' + jwt_token_of(User.objects.get(email=f'inst_{i}@snu.ac.kr'))
            setattr(cls, f"inst_{i}_token", token)

        cls.part = UserFactory(
            username='part',
            password='password',
            first_name='first_2',
            last_name='last_2',
            email='part@snu.ac.kr',
            is_participant=True
        )
        cls.part_token = 'JWT ' + jwt_token_of(User.objects.get(email='part@snu.ac.kr'))

        cls.partinst = UserFactory(
            username='partinst',
            password='password',
            first_name='first_3',
            last_name='last_3',
            email='partinst@snu.ac.kr',
            is_instructor=True,
            is_participant=True
        )
        cls.partinst_token = 'JWT ' + jwt_token_of(User.objects.get(email='partinst@snu.ac.kr'))

    def test_post_user_participant_byNoneParticipant(self):
        
        # Test with different body - changing "accepted" and "university"
        for i in range(1,4):
            if i==0 : request_data = {}
            elif i==1 : request_data = {"accepted" : "False",}
            else : request_data = {"university": "서울대학교",}

            with transaction.atomic():
                response = self.client.post('/api/v1/user/participant/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            data = response.json()
            self.assertEqual(data['username'], f"inst_{i}")
            self.assertEqual(data['email'], f"inst_{i}@snu.ac.kr")
            self.assertEqual(data['first_name'], f'first')
            self.assertEqual(data['last_name'], f'last')
            self.assertIn("last_login", data)
            self.assertIn("date_joined", data)
            self.assertIn("participant", data)
            
            participant_data = data.get("participant")
            self.assertIn("id", participant_data)
            self.assertIn("seminars", participant_data)

            if i==0 : 
                self.assertEqual(participant_data['university'], "")
                self.assertEqual(participant_data['accepted'], True)
            elif i==1 :
                self.assertEqual(participant_data['university'], "")
                self.assertEqual(participant_data['accepted'], False)
            else : 
                self.assertEqual(participant_data['university'], "서울대학교")
                self.assertEqual(participant_data['accepted'], True)

    def test_post_user_participant_byAlreadyParticipant(self):
        
        # User with ParticipantProfile
        with transaction.atomic():
            response = self.client.post('/api/v1/user/participant/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=self.part_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # User with InstructorProfile and ParticipantProfile
        with transaction.atomic():
            response = self.client.post('/api/v1/user/participant/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=self.partinst_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # User with InstructorProfile requests again
        with transaction.atomic():
            response = self.client.post('/api/v1/user/participant/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=self.inst_1_token)
            response = self.client.post('/api/v1/user/participant/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=self.inst_1_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)