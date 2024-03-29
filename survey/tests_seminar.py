import re
import json
from django.http import request
from factory.django import DjangoModelFactory
from django.db import transaction
from seminar.models import Seminar

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

        for i in range(1,6) : 
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

    def test_put_seminar_byInstructor(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']
        
        request_data = {}
        for i in range(5):
            if i==0: request_data["name"] = f"seminar_new"
            elif i==1: request_data["capacity"] = 20
            elif i==2: request_data["count"] = 10
            elif i==3: request_data["time"] = "16:30"
            else: request_data["online"] = "False"
            
            with transaction.atomic():
                response = self.client.put(f'/api/v1/seminar/{seminar_id}/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                        data=request_data)
            data = response.json()
            #print("****** : \n", json.dumps(data, ensure_ascii = False, indent=4))
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            if i>=0: self.assertEqual(data["name"], f"seminar_new")
            if i>=1: self.assertEqual(data["capacity"], 20)
            if i>=2: self.assertEqual(data["count"], 10)
            if i>=3: self.assertEqual(data["time"], "16:30")
            if i>=4: self.assertEqual(data["online"], False)

    def test_put_seminar_withWrongBody(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']
        
        request_data = {}
        for i in range(5):
            if i==0: request_data["name"] = ""
            elif i==1: request_data["capacity"] = 0
            elif i==2: request_data["count"] = 0
            elif i==3: request_data["time"] = "16:30:00"
            else: request_data["online"] = ""
            
            with transaction.atomic():
                response = self.client.put(f'/api/v1/seminar/{seminar_id}/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                        data=request_data)
            data = response.json()
            #print("****** : \n", json.dumps(data, ensure_ascii = False, indent=4))
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Seminar does not exist
        with transaction.atomic():
                response = self.client.put(f'/api/v1/seminar/100/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                        data=request_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_seminar_byWrongUser(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }
        
        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        with transaction.atomic():
            response = self.client.put(f'/api/v1/seminar/{seminar_id}/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)    
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            request_data = {
                "role" : "participant",
            }
            response = self.client.post('/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    )    
        with transaction.atomic():
            response = self.client.put(f'/api/v1/seminar/{seminar_id}/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        with transaction.atomic():
            response = self.client.put(f'/api/v1/seminar/{seminar_id}/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_2_token"),
                                    data=request_data)    
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   
    def test_put_seminar_capacityError(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 5,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        # 5 users are participants
        request_data = {
            "role" : "participant",
        }
        for i in range(1,6):
            with transaction.atomic():
                response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_{i}_token"),
                                        data=request_data)
        # participant count is 5, but update capacity is 4
        request_data = {
            "capacity" : 4,
        }
        with transaction.atomic():
            response = self.client.put(f'/api/v1/seminar/{seminar_id}/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # after 1 user dropped,
        # participant count is 4
        # so changing capacity to 4 should return 200_OK
        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    )
        request_data = {
            "capacity" : 4,
        }
        with transaction.atomic():
            response = self.client.put(f'/api/v1/seminar/{seminar_id}/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
                #print(json.dumps(response.json(), ensure_ascii=False, indent=4))    
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
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
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        seminar_id = data['id']

        # try with different user
        with transaction.atomic():
            response = self.client.get(f'/api/v1/seminar/{seminar_id}/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_2_token"),
                                    data=request_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data['name'], f"seminar_1")
        self.assertEqual(data['capacity'], 10)
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['time'], "14:30")
        
        instructors_data = data.get("instructors")[0]
        self.assertIn("id", instructors_data)
        self.assertEqual(instructors_data['username'], f"inst_1")
        self.assertEqual(instructors_data['email'], f"inst_1@snu.ac.kr")
        self.assertEqual(instructors_data['first_name'], f'first')
        self.assertEqual(instructors_data['last_name'], f'last')
        self.assertIn("joined_at", instructors_data)
        self.assertIn("participants", data)
        self.assertEqual(data['online'], True)

# GET /api/v1/seminar/
class GetSeminarList(TestCase):
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

        for i in range(1,10) : 
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

    def test_get_seminar_list(self):
        for i in range(1,4):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10+i,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)
            data = response.json()
            seminar_id = data['id']
            request_data = {
                "role" : "participant",
            }
            with transaction.atomic():
                response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_{2*i-1}_token"),
                                        data=request_data)   
            with transaction.atomic():
                response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_{2*i}_token"),
                                        data=request_data)                                     
            
        with transaction.atomic():
            response = self.client.get(f'/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    )
        data = response.json()
        for i in range(1,4):
            seminar_data = data[i-1]

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("id", seminar_data)
            self.assertEqual(seminar_data['name'], f"seminar_{4-i}")
            
            instructors_data = seminar_data.get("instructors")[0]
            self.assertIn("id", instructors_data)
            self.assertEqual(instructors_data['username'], f"inst_{4-i}")
            self.assertEqual(instructors_data['email'], f"inst_{4-i}@snu.ac.kr")
            self.assertEqual(instructors_data['first_name'], f'first')
            self.assertEqual(instructors_data['last_name'], f'last')
            self.assertIn("joined_at", instructors_data)
            self.assertEqual(seminar_data['participant_count'], 2)

    def test_get_seminar_list_withName(self):
        for i in range(1,4):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10+i,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)

            request_data = {
                "name" : f"queryName_{i}",
                "capacity" : 10+i,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)


        with transaction.atomic():
            response = self.client.get(f'/api/v1/seminar/?name=queryName', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    )

        data = response.json()
        for i in range(1,4):
            seminar_data = data[i-1]

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("id", seminar_data)
            self.assertEqual(seminar_data['name'], f"queryName_{4-i}")
            
            instructors_data = seminar_data.get("instructors")[0]
            self.assertIn("id", instructors_data)
            self.assertEqual(instructors_data['username'], f"inst_{4-i}")
            self.assertEqual(instructors_data['email'], f"inst_{4-i}@snu.ac.kr")
            self.assertEqual(instructors_data['first_name'], f'first')
            self.assertEqual(instructors_data['last_name'], f'last')
            self.assertIn("joined_at", instructors_data)
            self.assertEqual(seminar_data['participant_count'], 0)

    def test_get_seminar_list_withName_noMatching(self):
        for i in range(1,4):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10+i,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)

        with transaction.atomic():
            response = self.client.get(f'/api/v1/seminar/?name=queryName', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    )

        data = response.json()
        self.assertEqual(data, [])

    def test_get_seminar_list_earliest(self):
        for i in range(1,4):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10+i,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)
            data = response.json()
            seminar_id = data['id']
            request_data = {
                "role" : "participant",
            }
            with transaction.atomic():
                response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_{2*i-1}_token"),
                                        data=request_data)   
            with transaction.atomic():
                response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_{2*i}_token"),
                                        data=request_data)                                     
            
        with transaction.atomic():
            response = self.client.get(f'/api/v1/seminar/?order=earliest', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    )
        data = response.json()
        for i in range(1,4):
            seminar_data = data[i-1]

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("id", seminar_data)
            self.assertEqual(seminar_data['name'], f"seminar_{i}")
            
            instructors_data = seminar_data.get("instructors")[0]
            self.assertIn("id", instructors_data)
            self.assertEqual(instructors_data['username'], f"inst_{i}")
            self.assertEqual(instructors_data['email'], f"inst_{i}@snu.ac.kr")
            self.assertEqual(instructors_data['first_name'], f'first')
            self.assertEqual(instructors_data['last_name'], f'last')
            self.assertIn("joined_at", instructors_data)
            self.assertEqual(seminar_data['participant_count'], 2)

    def test_get_seminar_list_earliestwithName(self):
        for i in range(1,4):
            request_data = {
                "name" : f"seminar_{i}",
                "capacity" : 10+i,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)

            request_data = {
                "name" : f"queryName_{i}",
                "capacity" : 10+i,
                "count" : 5,
                "time" : "14:30",
                "online" : "True",
            }
            with transaction.atomic():
                response = self.client.post('/api/v1/seminar/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"inst_{i}_token"),
                                        data=request_data)


        with transaction.atomic():
            response = self.client.get(f'/api/v1/seminar/?order=earliest&name=queryName', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    )

        data = response.json()
        for i in range(1,4):
            seminar_data = data[i-1]

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn("id", seminar_data)
            self.assertEqual(seminar_data['name'], f"queryName_{i}")
            
            instructors_data = seminar_data.get("instructors")[0]
            self.assertIn("id", instructors_data)
            self.assertEqual(instructors_data['username'], f"inst_{i}")
            self.assertEqual(instructors_data['email'], f"inst_{i}@snu.ac.kr")
            self.assertEqual(instructors_data['first_name'], f'first')
            self.assertEqual(instructors_data['last_name'], f'last')
            self.assertIn("joined_at", instructors_data)
            self.assertEqual(seminar_data['participant_count'], 0)

# POST /api/v1/seminar/{seminar_id}/user/
class PostSeminarUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1,4): 
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

        for i in range(1,4): 
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

        user = UserFactory(
            username=f"partinst",
            password='password',
            first_name='first',
            last_name='last',
            email=f'partinst@snu.ac.kr',
            is_participant=True,
            is_instructor=True
        )
        setattr(cls, f"partinst", user)
        token = 'JWT ' + jwt_token_of(User.objects.get(email=f'partinst@snu.ac.kr'))
        setattr(cls, f"partinst_token", token)
            
    def test_post_seminar_user_correctRole(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {
            "role" : "participant",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        #print(json.dumps(data, ensure_ascii = False, indent=4))
        self.assertIn("id", data)
        self.assertEqual(data['name'], f"seminar_1")
        self.assertEqual(data['capacity'], 10)
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['time'], "14:30")
        self.assertEqual(data['online'], True)
        
        participants_data = data.get("participants")[0]
        self.assertIn("id", participants_data)
        self.assertEqual(participants_data['username'], f"part_1")
        self.assertEqual(participants_data['email'], f"part_1@snu.ac.kr")
        self.assertEqual(participants_data['first_name'], f'first')
        self.assertEqual(participants_data['last_name'], f'last')
        self.assertIn("joined_at", participants_data)
        self.assertEqual(participants_data['is_active'], True)
        self.assertEqual(participants_data['dropped_at'], None)

        request_data = {
            "role" : "instructor",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_2_token"),
                                    data=request_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data['name'], f"seminar_1")
        self.assertEqual(data['capacity'], 10)
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['time'], "14:30")
        self.assertEqual(data['online'], True)
        
        instructors_data = data.get("instructors")[1]
        self.assertIn("id", instructors_data)
        self.assertEqual(instructors_data['username'], f"inst_2")
        self.assertEqual(instructors_data['email'], f"inst_2@snu.ac.kr")
        self.assertEqual(instructors_data['first_name'], f'first')
        self.assertEqual(instructors_data['last_name'], f'last')
        self.assertIn("joined_at", instructors_data)

    def test_post_seminar_user_wrongRole(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {    
            "role" : "foobar",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        request_data = {
            "role" : "instructor",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_2_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        request_data = {
            "role" : "participant",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_2_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_post_seminar_noMatchingId(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        request_data = {
            "role" : "participant",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/100/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_2_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_seminar_user_withNotAcceptedParticipant(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        self.part_1.participant.accepted = False
        self.part_1.participant.save()
        self.part_1.save()

        request_data = {    
            "role" : "participant",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_seminar_user_fullCapacity(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 2,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {
            "role" : "participant",
        }

        # capacity is 2, but 3 users are applying
        for i in range(1,4):
            with transaction.atomic():
                response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_{i}_token"),
                                        data=request_data)
            #print("part count : ", Seminar.objects.get(id=seminar_id).participant_count)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
    
    def test_post_seminar_user_alreadyInstructor(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }
        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        request_data = {
            "name" : f"seminar_2",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }
        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_2_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {
            "role" : "instructor",
        }
        # inst_1 is applying another seminar
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        data = response.json()
        #print(json.dumps(data, ensure_ascii = False, indent=4))

    def test_post_seminar_user_alreadyInSeminar(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }
        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"partinst_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {
            "role" : "instructor",
        }
        # partinst is applying his/her seminar as an instructor
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"partinst_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_data = {
            "role" : "participant",
        }
        # partinst is applying his/her seminar as a participant
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"partinst_token"),
                                    data=request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_data = {
            "role" : "participant",
        }
        # double applying as a participant
        for i in range(2):
            with transaction.atomic():
                response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                        content_type='application/json', 
                                        HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                        data=request_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        #print(json.dumps(data, ensure_ascii = False, indent=4))

# DELETE /api/v1/seminar/{seminar_id}/user/
class DeleteSeminarUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(1,4): 
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

        for i in range(1,4): 
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

        user = UserFactory(
            username=f"partinst",
            password='password',
            first_name='first',
            last_name='last',
            email=f'partinst@snu.ac.kr',
            is_participant=True,
            is_instructor=True
        )
        setattr(cls, f"partinst", user)
        token = 'JWT ' + jwt_token_of(User.objects.get(email=f'partinst@snu.ac.kr'))
        setattr(cls, f"partinst_token", token)
            
    def test_delete_seminar_user(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {
            "role" : "participant",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)
        
        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        #print(json.dumps(data, ensure_ascii = False, indent=4))
        self.assertIn("id", data)
        self.assertEqual(data['name'], f"seminar_1")
        self.assertEqual(data['capacity'], 10)
        self.assertEqual(data['count'], 5)
        self.assertEqual(data['time'], "14:30")
        self.assertEqual(data['online'], True)
        
        participants_data = data.get("participants")[0]
        self.assertIn("id", participants_data)
        self.assertEqual(participants_data['username'], f"part_1")
        self.assertEqual(participants_data['email'], f"part_1@snu.ac.kr")
        self.assertEqual(participants_data['first_name'], f'first')
        self.assertEqual(participants_data['last_name'], f'last')
        self.assertIn("joined_at", participants_data)
        self.assertEqual(participants_data['is_active'], False)
        self.assertNotEqual(participants_data['dropped_at'], None)

    def test_delete_seminar_user_noMatchingId(self):
        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/100/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_2_token"),
                                    )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_seminar_user_instructorNotAllowed(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_seminar_user_notInSeminar(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_seminar_user_droppedReapply(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {
            "role" : "participant",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)
        
        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    )
        
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)
                                    
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_seminar_user_droppedRedrop(self):
        request_data = {
            "name" : f"seminar_1",
            "capacity" : 10,
            "count" : 5,
            "time" : "14:30",
            "online" : "True",
        }

        with transaction.atomic():
            response = self.client.post('/api/v1/seminar/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"inst_1_token"),
                                    data=request_data)
        data = response.json()
        seminar_id = data['id']

        request_data = {
            "role" : "participant",
        }
        with transaction.atomic():
            response = self.client.post(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    data=request_data)
        
        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    )
        
        with transaction.atomic():
            response = self.client.delete(f'/api/v1/seminar/{seminar_id}/user/', 
                                    content_type='application/json', 
                                    HTTP_AUTHORIZATION=getattr(self,f"part_1_token"),
                                    )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)