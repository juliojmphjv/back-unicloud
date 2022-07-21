from unicloud_sales.models import Opportunity, SalesRelatioshipFlow, ResourceOfOpportunity
from rest_framework import viewsets
from rest_framework.permissions import IsPartner, IsRoot
from unicloud_customers.models import Customer, UserCustomer
from unicloud_customers.receita_federal import ConsultaReceita
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from logs.setup_log import logger
from unicloud_customers.customers import CustomerObject
from .serializers import PartnerOpportunitiesListSerializer
from django.core import serializers

class OpportunityRegister(viewsets.ViewSet):
    permission_classes = (IsPartner,)

    def create(self, request):
        creation_status = None
        try:
            Customer.objects.get(cnpj=request.data['cnpj'])
            creation_status = True
            logger.info('Customer already exists.')
            return Response({'Status': 'Customer already exists in our base, creating the opportunity request.'})
        except Customer.DoesNotExist:
            logger.info('Customer doesnt exist, creating the customer')
            logger.info(ConsultaReceita(request.data['cnpj']))
            consulta_receita = ConsultaReceita(request.data['cnpj'])

            if consulta_receita.get_data()['status'] != 'ERROR':
                consulta_receitafederal = ConsultaReceita(request.data['cnpj'])
                customer_data = consulta_receitafederal.get_data()
                logger.info(f'org data from receita: {customer_data}')
                the_customer = Customer.objects.create(razao_social=customer_data['nome'], telefone=customer_data['telefone'], email=customer_data['email'], bairro=customer_data['bairro'], logradouro=customer_data['logradouro'], numero=customer_data['numero'], cep=customer_data['cep'], municipio=customer_data['municipio'], nome_fantasia=customer_data['fantasia'], natureza_juridica=customer_data['natureza_juridica'], estado=customer_data['uf'], cnpj=customer_data['cnpj'], type='customer')
                the_customer.save()
                creation_status = True
                logger.info('Customer Created!')
                return Response({'Status': 'Customer created, creating the opportunity request.'})
            creation_status = False
            return Response(consulta_receita.get_data())
        finally:
            if creation_status:
                logger.info('Creating the opportunity request')
                requester_organzation_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
                logger.info(f'requester org id: {requester_organzation_id}')
                requester_organization_instance = Customer.objects.get(id=requester_organzation_id)
                logger.info(f'requester org instance: {requester_organization_instance}')
                customer = Customer.objects.get(cnpj=request.data['cnpj'])
                logger.info(f'getting the customer: {customer}')
                if not Opportunity.objects.filter(partner=requester_organization_instance, customer=customer, status='opportunity_pending'):
                    opportunity = Opportunity.objects.create(partner=requester_organization_instance, customer=customer, opportunity_description=request.data['description'], user=request.user)
                    opportunity.save()
                    logger.info('Opportunity request created.')

                    for resource in request.data['resources_ids']:
                        resource_of_opportunity = ResourceOfOpportunity.objects.create(resource_id=resource, opportunity=opportunity)
                        resource_of_opportunity.save()

                    activity = SalesRelatioshipFlow.objects.create(partner=requester_organization_instance, customer=customer, author=request.user, description=request.data['description'])
                    activity.save()

    def retrieve(self, request):
        partner = CustomerObject(request)
        opportunities = Opportunity.objects.filter(partner=partner.get_customer_object().id)
        for opportunity in opportunities:
            opportunity.resources = []
            opportunity.history = []
            resources = ResourceOfOpportunity.objects.filter(opportunity=opportunity)
            for resource in resources:
                opportunity.resources.append({'resource_name': resource.resource.resource_name, 'resource_id': resource.resource.id})
            history = SalesRelatioshipFlow.objects.filter(partner=partner.get_customer_object().id, customer=opportunity.customer.id)
            for activity in history:
                opportunity.history.append({'author': activity.author.username, 'description': activity.description, 'date': activity.date, 'activity_id': activity.id})

        serializers = PartnerOpportunitiesListSerializer(opportunities, many=True)

        return Response(serializers.data)

class OpportunityReview(viewsets.ViewSet):
    permission_classes = (IsRoot, )

    def retrieve(self, request):
        opportunities = Opportunity.objects.all()
