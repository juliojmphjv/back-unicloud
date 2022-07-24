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
            organization = CustomerObject(request).get_customer_object()
            customers = Customer.objects.filter(type='customers')
            partners = Customer.objects.filter(type='partner')
            pods = ZadaraPods.objects.all()
            dashboard = {
                'customers': [],
                'partners': [],
                'pods': [],
            }

            if pods:
                for pod in pods:
                    engenheiro = DashboardFactory(pod.name)
                    zad = ZadaraDashboard(pod, organization)
                    dashboard['pods'].append(engenheiro.get_dasboard(zad))
                    logger.info(dashboard)

            dashboard['customers'] = customers
            dashboard['partners'] = partners

            logger.info(dashboard)

            serializer = DashboardSerializer(dashboard)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)

class Dashboard(viewsets.ViewSet):
    permission_classes = (IsPartner, )

    def get_dashboard(self, request):
        try:
            organization = CustomerObject(request).get_customer_object()
            customers_relationhips = CustomerRelationship.objects.filter(partner=organization)
            customers_ids = []
            for customer in customers_relationhips:
                customers_ids.append(customer.id)
            customers = Customer.objects.filter(customer__partner_id__in=customers_ids)
            logger.info(customers)
            # dashboard = {
            #     'customers': customers,
            # }

            # logger.info(dashboard)
            return Response({'teste':'teste'})
        except Exception as error:
            logger.error(error)
            return Response({'erro': 'erro'})