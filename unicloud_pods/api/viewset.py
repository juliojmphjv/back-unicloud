from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
from ..models import ZadaraPods
from .serializers import UniCloudZadaraPodsSerializer
import bleach
from logs.setup_log import logger

class ZadaraPodsViewSet(viewsets.ViewSet):
    permission_classes(IsAdminUser,)

    def create(self, request):
        try:
            new_pod = ZadaraPods.objects.create(name=bleach.clean(request.data['name']), location=bleach.clean(request.data['location']), type=bleach.clean(request.data['type']), url_base=bleach.clean(request.data['url_base']), pod_user=bleach.clean(request.data['pod_user']), pod_password=bleach.clean(request.data['pod_password']), domain_tenant=bleach.clean(request.data['domain_tenant']), project_id=bleach.clean(request.data['project_id']))
            new_pod.save()
            serializer = UniCloudZadaraPodsSerializer(new_pod)
            return Response(serializer.data)
        except Exception as error:
            logger.info(error)

    def retrieve_list(self, request):

        try:
            pods = ZadaraPods.objects.all()
            serializer = UniCloudZadaraPodsSerializer(pods, many=True)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})