from rest_framework import serializers


class UniCloudZadaraPodsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    location = serializers.CharField(max_length=100)
    type = serializers.CharField(max_length=50)
    url_base = serializers.CharField(max_length=500)
    pod_user = serializers.CharField(max_length=50)
    pod_password = serializers.CharField(max_length=150)
    project_id = serializers.CharField(max_length=150)
    domain_tenant = serializers.CharField(max_length=50)