from rest_framework import serializers

class PodSerializer(serializers.Serializer):
    pod_name = serializers.CharField(max_length=15)
    location = serializers.JSONField()
    total_spare_nodes = serializers.IntegerField()
    total_nodes = serializers.IntegerField()
    total_memory = serializers.IntegerField()
    total_physical_cpu = serializers.IntegerField()
    total_vcores = serializers.IntegerField()

class DashboardSerializer(serializers.Serializer):
    customers = serializers.JSONField()
    partners = serializers.JSONField()
    total_nodes = serializers.IntegerField()
    total_memory = serializers.IntegerField()
    total_physical_cpu = serializers.IntegerField()
    total_vcores = serializers.IntegerField()
    total_pods = serializers.IntegerField()
    total_spare_nodes = serializers.IntegerField()
    pods = PodSerializer(required=True, many=True)
