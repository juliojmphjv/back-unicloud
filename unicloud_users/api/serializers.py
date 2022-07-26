from rest_framework.serializers import ModelSerializer
from unicloud_users.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

class LoginTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff
        token['email'] = user.email
        # ...
        return token

class MenuSerializer(serializers.Serializer):
    menu = serializers.JSONField()

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

class UserProfileSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=25)
    address = serializers.CharField(max_length=250)
    city = serializers.CharField(max_length=150)
    state = serializers.CharField(max_length=150)
    country = serializers.CharField(max_length=150)

class UserListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    userprofile = UserProfileSerializer(required=True)
    username = serializers.EmailField()
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()

class InvitedUserListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    created_at = serializers.DateTimeField()



class InvitedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    token = serializers.CharField(max_length=500)
    email = serializers.EmailField()
    razao_social = serializers.CharField()
    is_valid = serializers.BooleanField()

class InvalidTokenSerializer(serializers.Serializer):
    is_valid = serializers.BooleanField()