from rest_framework import serializers
from django.core.serializers.json import Serializer
from django.db.models import Manager
from logs.setup_log import logger

class ResourcesSerializer(serializers.Serializer):
    resource_name = serializers.CharField(max_length=150)
    resource_id = serializers.IntegerField()

class HistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    author = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=100000)
    date = serializers.DateTimeField()

class OpportunitySerializer(serializers.Serializer):
    opportunity_name = serializers.CharField(max_length=300)
    id = serializers.IntegerField()
    customer = serializers.CharField()
    opportunity_description = serializers.CharField(max_length=100000000000)
    user = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=50)
    request_date = serializers.DateTimeField()
    resources = ResourcesSerializer(required=True, many=True)

class OneOpportunitySerializer(serializers.Serializer):
    opportunity_name = serializers.CharField(max_length=300)
    id = serializers.IntegerField()
    customer = serializers.CharField()
    opportunity_description = serializers.CharField(max_length=100000000000)
    user = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=50)
    request_date = serializers.DateTimeField()
    resources = ResourcesSerializer(required=True, many=True)
    history = HistorySerializer(required=True, many=True)