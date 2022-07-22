from unicloud_sales.models import Opportunity, SalesRelatioshipFlow, ResourceOfOpportunity
from rest_framework import viewsets
from unicloud_customers.customer_permissions import IsPartner, IsRoot
from unicloud_customers.models import Customer, UserCustomer
from unicloud_customers.receita_federal import ConsultaReceita
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from logs.setup_log import logger
from unicloud_customers.customers import CustomerObject
from .serializers import OpportunitySerializer, OneOpportunitySerializer
from django.core import serializers
from error_messages import messages

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
                if not Opportunity.objects.filter(partner=requester_organization_instance, customer=customer, status__in=['opportunity_pending', 'approved']):
                    logger.info('Creating the opportunity...')
                    opportunity = Opportunity.objects.create(opportunity_name=['opportunity_name'], partner=requester_organization_instance, customer=customer, opportunity_description=request.data['description'], user=request.user)
                    opportunity.save()
                    logger.info('Opportunity request created.')

                    try:
                        logger.info('Creating the opportunity resources...')
                        for resource in request.data['resources_ids']:
                            resource_of_opportunity = ResourceOfOpportunity.objects.create(resource_id=resource, opportunity=opportunity)
                            resource_of_opportunity.save()
                        logger.info('resources created')
                    except Exception as error:
                        logger.error(error)

                    try:
                        logger.info('creating the activity in sales flow history')
                        activity = SalesRelatioshipFlow.objects.create(partner=requester_organization_instance, customer=customer, author=request.user, description=request.data['description'])
                        activity.save()
                        logger.info(f'sales flow history created {activity}')
                    except Exception as error:
                        logger.error(error)
                else: logger.error('this partner already have an opportunity in this customer pending or approved')
            else: logger.error('Error in customer Get or Creation')

    def retrieve(self, request):
        organization = CustomerObject(request)
        opportunities = None
        if organization.get_customer_object().type == 'root':
            opportunities = Opportunity.objects.all()
        elif organization.get_customer_object().type == 'partner':
            opportunities = Opportunity.objects.filter(partner=organization.get_customer_object().id)

        for opportunity in opportunities:
            opportunity.resources = []
            resources = ResourceOfOpportunity.objects.filter(opportunity=opportunity)
            for resource in resources:
                opportunity.resources.append({'resource_name': resource.resource.resource_name, 'resource_id': resource.resource.id})

        serializers = OpportunitySerializer(opportunities, many=True)

        return Response(serializers.data)

class OneOpportunity(viewsets.ViewSet):
    permission_classes(IsPartner, )

    def get_one_opportunity(self, request):
        try:
            organization = CustomerObject(request)
            opportunity = Opportunity.objects.get(id=request.data['opportunity_id'])

            if opportunity.partner.id == organization.get_customer_object().id:
                opportunity.resources = []
                resources = ResourceOfOpportunity.objects.filter(opportunity=opportunity)
                for resource in resources:
                    opportunity.resources.append(
                        {'resource_name': resource.resource.resource_name, 'resource_id': resource.resource.id})
                opportunity.history = []
                history = None
                if organization.get_customer_object().type == 'root':
                    history = SalesRelatioshipFlow.objects.filter(customer=opportunity.customer, opportunity=opportunity)
                elif organization.get_customer_object().type == 'partner':
                    history = SalesRelatioshipFlow.objects.filter(partner=organization.get_customer_object(), customer=opportunity.customer, opportunity=opportunity)
                for activity in history:
                    opportunity.history.append(activity)
                serializer = OneOpportunitySerializer(opportunity)
                return Response(serializer.data)
            else:
                logger.error('This organizations is not the opportunity owner')
                return Response(messages.permission_denied)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})




class OpportunityStatus(viewsets.ViewSet):
    permission_classes = (IsRoot, )

    def set_opportunity_status(self, request):
        try:
            opportunity = Opportunity.objects.get(id=request.data['opportunity_id'])
            opportunity.status = request.data['new_status']
            opportunity.save()
            resources = ResourceOfOpportunity.objects.filter(opportunity=opportunity)
            opportunity.resources = []
            for resource in resources:
                opportunity.resources.append(
                    {'resource_name': resource.resource.resource_name, 'resource_id': resource.resource.id})
            serializer = OpportunitySerializer(opportunity)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})
