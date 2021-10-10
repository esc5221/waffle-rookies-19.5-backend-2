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

# POST /api/v1/seminar/
class PostSeminar(TestCase):
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

        for i in range(1,4) : 
            user = UserFactory(
                username=f"part_{i}",
                password='password',
                first_name='first',
                last_name='last',
                email=f'part_{i}@snu.ac.kr',
                is_participant=True
            )
            setattr(cls, f"part_{i}", user)
            token = 'JWT ' + jwt_token_of(User.objects.get(email=f'part_{i}@snu.ac.kr'))
            setattr(cls, f"part_{i}_token", token)

    def test_post_seminar_byInstructor(self):
        for i in range(1,3):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }

            # test with various "online" value
            if i==1 : request_data["online"] = "False"
            elif i==2 : request_data.pop("online")
            else : pass 

            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            data = response.json()
            self.assertIn("id", data)
            self.assertEqual(data['name'], f"seminar_{i}")
            self.assertEqual(data['capacity'], 10)
            self.assertEqual(data['count'], 5)
            self.assertEqual(data['time'], "14:30")
            
            instructors_data = data.get("instructors")[0]
            self.assertIn("id", instructors_data)
            self.assertEqual(instructors_data['username'], f"inst_{i}")
            self.assertEqual(instructors_data['email'], f"inst_{i}@snu.ac.kr")
            self.assertEqual(instructors_data['first_name'], f'first')
            self.assertEqual(instructors_data['last_name'], f'last')
            self.assertIn("joined_at", instructors_data)
            self.assertIn("participants", data)

            if i==1 : self.assertEqual(data['online'], False)
            else : self.assertEqual(data['online'], True)

    def test_post_seminar_withWrongBody(self):
        for i in range(1,3):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            
            # test with wrong body cases
            if i==1 : request_data.pop("name")
            elif i==2 : request_data["name"] = ""
            elif i==3 : request_data["capacity"] = 0
            elif i==4 : request_data["count"] = 0
            elif i==5 : request_data["time"] = "14:30:00"

            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                        data=request_data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
   
    def test_post_seminar_byWrongUser(self):
        for i in range(1,2):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                        data=request_data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            
         

# PUT /api/v1/seminar/{seminar_id}/
@tag("todo")
class PutSeminar(TestCase):
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

        for i in range(1,4) : 
            user = UserFactory(
                username=f"part_{i}",
                password='password',
                first_name='first',
                last_name='last',
                email=f'part_{i}@snu.ac.kr',
                is_participant=True
            )
            setattr(cls, f"part_{i}", user)
            token = 'JWT ' + jwt_token_of(User.objects.get(email=f'part_{i}@snu.ac.kr'))
            setattr(cls, f"part_{i}_token", token)

    def test_post_seminar_byInstructor(self):
        for i in range(1,3):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }

            # test with various "online" value
            if i==1 : request_data["online"] = "False"
            elif i==2 : request_data.pop("online")
            else : pass 

            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            data = response.json()
            self.assertEqual(data['name'], f"seminar_{i}")
            self.assertEqual(data['capacity'], 10)
            self.assertEqual(data['count'], 5)
            self.assertEqual(data['time'], "14:30")
            
            instructors_data = data.get("instructors")[0]
            self.assertIn("id", instructors_data)
            self.assertEqual(instructors_data['username'], f"inst_{i}")
            self.assertEqual(instructors_data['email'], f"inst_{i}@snu.ac.kr")
            self.assertEqual(instructors_data['first_name'], f'first')
            self.assertEqual(instructors_data['last_name'], f'last')
            self.assertIn("joined_at", instructors_data)
            self.assertIn("participants", data)

            if i==1 : self.assertEqual(data['online'], False)
            else : self.assertEqual(data['online'], True)

    def test_post_seminar_withWrongBody(self):
        for i in range(1,3):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            
            # test with wrong body cases
            if i==1 : request_data.pop("name")
            elif i==2 : request_data["name"] = ""
            elif i==3 : request_data["capacity"] = 0
            elif i==4 : request_data["count"] = 0
            elif i==5 : request_data["time"] = "14:30:00"

            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                        data=request_data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
   
    def test_post_seminar_byWrongUser(self):
        for i in range(1,2):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                        data=request_data)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            
# GET /api/v1/seminar/{seminar_id}/
class GetSeminar(TestCase):
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

        for i in range(1,4) : 
            user = UserFactory(
                username=f"part_{i}",
                password='password',
                first_name='first',
                last_name='last',
                email=f'part_{i}@snu.ac.kr',
                is_participant=True
            )
            setattr(cls, f"part_{i}", user)
            token = 'JWT ' + jwt_token_of(User.objects.get(email=f'part_{i}@snu.ac.kr'))
            setattr(cls, f"part_{i}_token", token)

    def test_get_seminar_id(self):
        for i in range(1,2):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }

            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)
            
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            data = response.json()
            data['id']
            self.assertEqual(data['name'], f"seminar_{i}")
            self.assertEqual(data['capacity'], 10)
            self.assertEqual(data['count'], 5)
            self.assertEqual(data['time'], "14:30")
            
            instructors_data = data.get("instructors")[0]
            self.assertIn("id", instructors_data)
            self.assertEqual(instructors_data['username'], f"inst_{i}")
            self.assertEqual(instructors_data['email'], f"inst_{i}@snu.ac.kr")
            self.assertEqual(instructors_data['first_name'], f'first')
            self.assertEqual(instructors_data['last_name'], f'last')
            self.assertIn("joined_at", instructors_data)
            self.assertIn("participants", data)


# GET /api/v1/seminar/
class GetSeminarList(TestCase):
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

# POST /api/v1/seminar/{seminar_id}/user/
class PostSeminarUser(TestCase):
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

# DELETE /api/v1/seminar/{seminar_id}/user/
class DeleteSeminaruser(TestCase):
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