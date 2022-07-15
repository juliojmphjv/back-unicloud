from rest_framework import serializers

class ResourceTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    resource_type = serializers.CharField(max_length=50)

class ResourceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    resource_name = serializers.CharField(max_length=150)

class AssetsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    resource = serializers.CharField(max_length=50)
    qty = serializers.IntegerField()