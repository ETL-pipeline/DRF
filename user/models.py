from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
# Create your models here.
class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, login_id, name, age, gender, phone_number, password=None):
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
        user.save(using=self._db)
        return user
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    login_id = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    age = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    choices = [('M','Male'), ('F','Female')]
    gender = models.CharField(default='', max_length=2,choices=choices, null=False, blank=False)
    phone_number = models.CharField(default='', max_length=12, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    # 헬퍼 클래스 사용
    objects = UserManager()
    # 필수로 작성해야하는 field
    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['email', 'name', 'age', 'gender','phone_number']

    def __str__(self):
        return self.login_id

class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()