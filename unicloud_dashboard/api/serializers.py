from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    customers = serializers.JSONField()
    partners = serializers.JSONField()
    locations = serializers.JSONField()