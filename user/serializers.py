from .models import User, Blog
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            name = validated_data['name'],
            login_id = validated_data['login_id'],
            password = validated_data['password'],
            age = validated_data['age'],
            gender = validated_data['gender'],
            phone_number = validated_data['phone_number'],
        )
        return user
    class Meta:
        model = User
        fields = ['login_id', 'email', 'name', 'password', 'age', 'gender', 'phone_number']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'