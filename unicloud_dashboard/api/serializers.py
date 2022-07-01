from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    customers = serializers.JSONField()
    partners = serializers.JSONField()
    locations = serializers.JSONField()
    total_spare_nodes = serializers.IntegerField()
    number_of_pods = serializers.IntegerField()
    total_nodes = serializers.IntegerField()
    total_memory = serializers.IntegerField()
    total_fisical_cpu = serializers.IntegerField()
    total_vcores = serializers.IntegerField()