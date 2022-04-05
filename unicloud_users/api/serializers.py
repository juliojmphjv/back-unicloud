from rest_framework.serializers import ModelSerializer
from unicloud_users.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from ..menu import menu


class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'state', 'country', 'user_id')


class UserListSerializer(ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = (
        'id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'last_login', 'date_joined', 'userprofile')

    def create(self, validated_data):
        userprofile = validated_data.pop('userprofile')
        user = User.objects.create_user(**validated_data)
        profile = UserProfile(**userprofile, user_id=user.id)
        UserProfile.save(profile)
        return user

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
    def __init__(self):
        self.menu = menu
    def serialize_menu(self):
        return menu

