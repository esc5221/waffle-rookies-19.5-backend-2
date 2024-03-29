from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
class Seminar(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    time = models.TimeField()
    online = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    participant_count = models.PositiveIntegerField(default=0)

class UserSeminar(models.Model):
    user = models.ForeignKey(get_user_model(),related_name='userseminar', null=False, on_delete=models.CASCADE)
    seminar = models.ForeignKey(Seminar, related_name='userseminar', null=False, on_delete=models.CASCADE)
    role = models.CharField(max_length=20)

    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    dropped_at = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


