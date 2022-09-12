from rest_framework import serializers
from django.core.serializers.json import Serializer
from django.db.models import Manager
from logs.setup_log import logger
from decimal import Decimal

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
    customer_id = serializers.IntegerField()
    opportunity_description = serializers.CharField(max_length=100000000000)
    user = serializers.CharField(max_length=100)
    status = serializers.CharField(max_length=50)
    request_date = serializers.DateTimeField()
    resources = ResourcesSerializer(required=True, many=True)
    history = HistorySerializer(required=True, many=True)

class ComputeQuotationSerializer(serializers.Serializer):
    informal = serializers.FloatField()
    eleven_month_agreement = serializers.FloatField()
    thirtysix_month_agreement = serializers.FloatField()

class SubscriptionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    months = serializers.IntegerField()
    discount = serializers.IntegerField()

class CurrencySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    currency = serializers.CharField(max_length=5)
    unicloud_currency = serializers.DecimalField(default=0, max_digits=6, decimal_places=2)
    safety_margin = serializers.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0))
    ptax = serializers.FloatField()
    overpriced_unicloud_currency = serializers.DecimalField(default=0, max_digits=6, decimal_places=2)

class SetCurrencySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    currency = serializers.CharField(max_length=5)
    unicloud_currency = serializers.DecimalField(default=0, max_digits=6, decimal_places=2)
    safety_margin = serializers.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0))