from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
import bleach
from logs.setup_log import logger
from unicloud_pods.models import ZadaraPods
from unicloud_customers.models import Customer
from check_root.unicloud_check_root import CheckRoot
from .serializers import DashboardSerializer
from unicloud_pods.zadara import Zadara

class Dashboard(viewsets.ViewSet):
    permission_classes(IsAuthenticated, )

    def get_dashboard(self, request):
        requester = CheckRoot(request)
        dashboard = {
            'customers': [],
            'partners': [],
            'locations': [],
            'total_spare_nodes': 0,
            'number_of_pods': 0,

        }
        try:
            if requester.is_root():
                logger.info('Requester is root')
                try:
                    customers = Customer.objects.filter(type='customer')
                    partners = Customer.objects.filter(type='partner')
                    zadara_pods = ZadaraPods.objects.all()
                    dashboard['number_of_pods'] = len(zadara_pods)
                    for customer in customers:
                        dashboard['customers'].append(customer.razao_social)
                    for partner in partners:
                        dashboard['partners'].append(partner.razao_social)
                    for pod in zadara_pods:
                        vendor = Zadara(pod)
                        dashboard['locations'].append({pod.location: vendor.get_pods_geolocation(pod.location)})
                        dashboard['total_spare_nodes'] = pod.spare_nodes
                        zadara_data = vendor.get_zadara_pod_sparenodes()
                        for data in zadara_data:
                            for key in data.keys():
                                dashboard[key] = data[key]

                    serializer = DashboardSerializer(dashboard)
                    return Response(serializer.data)
                except Exception as error:
                    serializer = DashboardSerializer(dashboard)
                    logger.error(error)
                    return Response(serializer.errors)
            logger.info(requester.is_root())
            return Response({'dashboard': 'User Dashboard hasnt data available'})
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

