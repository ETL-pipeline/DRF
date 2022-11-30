from .models import User

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User

class SignupSirializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
    ),
    password = serializers.CharField(
        required = True,
        write_only = True,
        style = {'input_type': 'password'} 
    )
    password2 = serializers.CharField(
        write_only = True,
        required = True,
        style = {'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ('login_id','password', 'password2', 'name','email','age','gender','phone_number')
    
    def validate(self, data):
        
             
        if User.objects.filter(login_id=data['login_id']).exists():
            raise serializers.ValidationError({
                'login_id': '이미 존재하는 아이디입니다.'
                })

        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password" : "비밀번호가 맞지 않습니다."
            })
        
        return data

    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            name = validated_data['name'],
            login_id = validated_data['login_id'],
            password = validated_data['password'],
            age = validated_data['age'],
            gender = validated_data['gender'],
            phone_number = validated_data['phone_number'],
        )
        token = RefreshToken.for_user(user)
        user.set_password(validated_data['password'])
        user.refreshtoken = token
        user.save()
    
        return user
class SigninSirializer(serializers.ModelSerializer):
    login_id = serializers.CharField(
        required = True,
        write_only = True
    )
    password = serializers.CharField(
        required = True,
        write_only = True,
        style= {'input_type' : 'password'}
    )
    class Meta(object):
        model = User
        fields = ('login_id', 'password')

    def validate(self, data):
        login_id = data.get('login_id',None)
        password = data.get('password',None)

        if User.objects.filter(login_id=login_id).exists():
            user = User.objects.get(login_id=login_id)

            if not user.check_password(password):
                raise serializers.ValidationError('Check Your login_id or Password')
        else:
            raise serializers.ValidationError("User does not exist")
        
        token = RefreshToken.for_user(user=user)
        data = {
            'user' : user.id,
            'refresh_token' : str(token),
            'access_token' : str(token.access_token)
        }
        return data