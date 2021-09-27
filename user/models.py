from django.db import models

# Create your models here.
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, UserManager
from django.utils import timezone

class ParticipantProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    university = models.CharField(max_length=50, blank=True)
    accepted = models.BooleanField(default=True)

class InstructorProfile(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.CharField(max_length=50, blank=True)
    year = models.PositiveIntegerField(null=True)

class CustomUserManager(BaseUserManager):

    # CustomUserManager 가 위에 임포트해두고 쓰지 않는 UserManager 와 어떻게 다른지 파악하면서 보시면 좋을 것 같습니다.
    # 이메일 기반으로 인증 방식을 변경하기 위한 구현입니다.

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일을 설정해주세요.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):

        # setdefault -> 딕셔너리에 key가 없을 경우 default로 값 설정
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        # TODO
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True or extra_fields.get('is_superuser') is not True:
            raise ValueError('권한 설정이 잘못되었습니다.')

        # TODO
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    # TODO 
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=128, verbose_name='password')
    is_superuser = models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    last_login = models.DateTimeField(default=timezone.now)
    participant = models.OneToOneField(ParticipantProfile, related_name='participant', null=True, blank=True, on_delete=models.CASCADE)
    instructor = models.OneToOneField(InstructorProfile, related_name='instructor', null=True, blank=True, on_delete=models.CASCADE)
    role = models.CharField(max_length=30)

    objects = CustomUserManager()

    # 유저 필드를 작성해주세요.
    #  기존 과제 0, 과제 1에서 사용하던 유저 정보를 모두 포함하고 있어야 합니다.
    #  1. 이제 이메일은 유저마다 고유한 식별자가 되어야 합니다. 필드 선언 시 적절한 옵션을 지정해주세요
    #  2. 위에 선언한 CustomManager를 이 모델의 매니저로 선언하여야 합니다.

    # 해당 필드에 대한 설명은 부모 AbstractBaseUser 클래스 참고
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.email

