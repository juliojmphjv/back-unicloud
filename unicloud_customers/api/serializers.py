from rest_framework import serializers
from ..models import InvitedUser
from rest_framework.fields import CurrentUserDefault

class InvitedUserSerializer(serializers.Serializer):
    teste = serializers.CharField(max_length=20)


class CustomerSerializer(serializers.Serializer):
    teste = serializers.CharField(max_length=20)