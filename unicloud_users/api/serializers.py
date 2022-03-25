from rest_framework.serializers import ModelSerializer
from unicloud_users.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('phone', 'addrees', 'city', 'state', 'country', 'user_id')

class UserSerializer(ModelSerializer):
    userprofile = UserProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'userprofile', 'last_login', 'date_joined')

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
        print(token)
        return token