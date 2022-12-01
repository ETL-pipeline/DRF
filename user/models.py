from django.db import models
from model_utils import Choices
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, login_id, name, age, gender, phone_number, password=None):
        """

        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError('must have user email')
        if not name:
            raise ValueError('must have user name')
        if not login_id:
            raise ValueError('must have user login_id')
        if not age:
            raise ValueError('must have user age')
        if not gender:
            raise ValueError('must have user gender')
        if not phone_number:
            raise ValueError('must have user phone_number')
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            login_id = login_id,
            age = age,
            gender = gender,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login_id, name, age, gender, phone_number, password=None):
    	
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        user = self.create_user(
            email,
            password = password,
            name = name,
            age = age,
            login_id = login_id,
            gender = gender,
            phone_number = phone_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# AbstractBaseUser를 상속해서 유저 커스텀
class User(AbstractBaseUser, PermissionsMixin):
    
    id = models.AutoField(primary_key=True)
    login_id = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)

    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    age = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    choices = [('M','Male'), ('F','Female')]
    gender = models.CharField(default='', max_length=2,choices=choices, null=False, blank=False)

    phone_number = models.CharField(default='', max_length=12, null=False, blank=False)
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는 login_id으로 설정 (아이디 로 로그인)
    USERNAME_FIELD = 'login_id'

    REQUIRED_FIELDS = ['email', 'name', 'age', 'gender','phone_number']

    def __str__(self):
        return self.login_id

class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()