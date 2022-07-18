from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import ResourcesType, Resource, Assets
from .serializer import ResourceTypeSerializer, ResourceSerializer, AssetsSerializer
from rest_framework.response import Response
from logs.setup_log import logger
from unicloud_contracts.models import Contracts

class ResourceViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def create(self, request):
        try:
            type = ResourcesType.objects.get(id=request.data['type_id'])
            resource = Resource.objects.create(resource_name=request.data['resource'], type=type)
            resource.save()
            serializer = ResourceSerializer(resource)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def retrieve(self, request):
        try:
            resources = Resource.objects.all()
            serializer = ResourceSerializer(resources, many=True)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def delete(self, request):
        try:
            resource = Resource.objects.get(id=request.data['resource_id'])
            resource.delete()
            return Response({'status': 'deleted'})
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def update(self, request):
        try:
            resource = Resource.objects.get(id=request.data['resource_id'])
            resource.resource_name = request.data['new_resource_name']
            resource.save()
            serializer = ResourceSerializer(resource)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)

class ResourceTypeViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def create(self, request):
        try:
            type = ResourcesType.objects.create(resource_type=request.data['resource_type'])
            type.save()
            serializer = ResourceTypeSerializer(type)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def retrieve(self, request):
        try:
            types = ResourcesType.objects.all()
            serializer = ResourceTypeSerializer(types, many=True)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def delete(self, request):
        try:
            type = ResourcesType.objects.get(id=request.data['resource_type_id'])
            type.delete()
            return Response({'status': 'deleted'})
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def update(self, request):
        try:
            type = ResourcesType.objects.get(id=request.data['resource_type_id'])
            type.resource_type = request.data['new_resource_type']
            type.save()
            serializer = ResourceTypeSerializer(type)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

class AssetsViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def create(self, request):
        try:
            contract = Contracts.objects.get(id=request.data['contract_id'])
            resource = Resource.objects.get(id=request.data['resource_id'])
            asset = Assets.objects.create(contract=contract, resource=resource, qty=request.data['qty'])
            asset.save()
            serializer = AssetsSerializer(asset)
            return Response(serializer.data)
        except Exception as error:
            return Response({'error': error})

    def retrieve(self, request):
        try:
            resources = Resource.objects.filter(assets__contract_id=request.data['contract_id'])
            serializer = AssetsSerializer(resources, many=True)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})