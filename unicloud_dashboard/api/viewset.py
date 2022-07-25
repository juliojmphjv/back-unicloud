from rest_framework.permissions import IsAuthenticated, IsAdminUser
from unicloud_customers.customer_permissions import IsCustomer, IsRoot, IsPartner
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.models import User
import bleach
from logs.setup_log import logger
from unicloud_pods.models import ZadaraPods
from unicloud_customers.models import Customer
from check_root.unicloud_check_root import CheckRoot
from .serializers import DashboardSerializer
from unicloud_pods.zadara.zadara import Zadara
from unicloud_customers.customers import CustomerObject
from unicloud_customers.models import CustomerRelationship
from unicloud_dashboard.dashboards.zadara_dash import ZadaraDashboard
from unicloud_dashboard.factory.factory import DashboardFactory

class RootDashboard(viewsets.ViewSet):
    permission_classes = (IsRoot,)

    def get_dashboard(self, request):
        try:
            logger.info('in try')
            organization = CustomerObject(request).get_customer_object()
            logger.info(f'getting org: {organization}')
            customers = Customer.objects.filter(type='customers')
            logger.info(f'lista de customers: {customers}')
            partners = Customer.objects.filter(type='partner')
            logger.info(f'lista de partners: {partners}')

            pods = ZadaraPods.objects.all()
            logger.info(f'Getting pods: {pods}')
            dashboard = {
                'customers': [],
                'partners': [],
                'pods': [],
                'total_nodes': 0,
                'total_memory': 0,
                'total_physical_cpu': 0,
                'total_vcores': 0,
                'total_pods': 0,
                'total_spare_nodes': 0,
            }
            logger.info(dashboard)
            total_allpods_memory = []
            total_allpods_cpus = []
            total_allpods_vcores = []
            total_allpods_nodes = []
            total_allpods_sparenodes = []

            if pods:
                logger.info('has Pods')
                for pod in pods:
                    logger.info(f'in pod: {pod.name}')
                    engenheiro = DashboardFactory(pod.name)
                    zadara = ZadaraDashboard(pod, organization)
                    pod_data = engenheiro.get_dasboard(zadara)
                    logger.info(f'pod data: {pod_data}')
                    dashboard['pods'].append(pod_data)
                    total_allpods_memory.append(pod_data['total_memory'])
                    total_allpods_cpus.append(pod_data['total_physical_cpu'])
                    total_allpods_vcores.append(pod_data['total_vcores'])
                    total_allpods_nodes.append(pod_data['total_nodes'])
                    total_allpods_sparenodes.append(pod_data['total_spare_nodes'])

                dashboard['total_memory'] = sum(total_allpods_memory)
                dashboard['total_physical_cpu'] = sum(total_allpods_cpus)
                dashboard['total_vcores'] = sum(total_allpods_vcores)
                dashboard['total_pods'] = len(pods)
                dashboard['total_spare_nodes'] = sum(total_allpods_sparenodes)

            dashboard['customers'] = customers
            dashboard['partners'] = partners

            logger.info(f'Final Dash: {dashboard}')

            try:
                serializer = DashboardSerializer(dashboard)
                logger.info(f'Dash serialized: {serializer.data}')
                return Response(serializer.data)
            except Exception as error:
                logger.error(error)

        except Exception as error:
            logger.error(error)

class PartnerDashboard(viewsets.ViewSet):
    permission_classes = (IsPartner, )

    def get_dashboard(self, request):
        try:
            return Response({'status': 'doesnt have data'})
        except Exception as error:
            logger.error(error)
            return Response({'erro': 'erro'})

class CustomerDashboard(viewsets.ViewSet):
    permission_classes = (IsPartner, )

    def get_dashboard(self, request):
        try:
            return Response({'status': 'doesnt have data'})
        except Exception as error:
            logger.error(error)
            return Response({'erro': 'erro'})