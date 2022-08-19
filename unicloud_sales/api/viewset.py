from unicloud_sales.models import Opportunity, SalesRelatioshipFlow, ResourceOfOpportunity
from rest_framework import viewsets
from unicloud_customers.customer_permissions import IsPartner, IsRoot
from unicloud_customers.models import Customer, UserCustomer
from unicloud_customers.receita_federal import ConsultaReceita
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from logs.setup_log import logger
from unicloud_customers.customers import CustomerObject
from .serializers import OpportunitySerializer, OneOpportunitySerializer, ComputeQuotationSerializer, HistorySerializer
from django.core import serializers
from error_messages import messages
from unicloud_customers.receita_federal import ConsultaReceita
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from ..calculator_tool import Calculator

class OpportunityRegister(viewsets.ViewSet):
    permission_classes = (IsPartner,)

    def create(self, request):
        creation_status = False
        cnpj = None
        customer_data = None
        customer_id = None
        try:
            consulta_receitafederal = ConsultaReceita(request.data['cnpj'])
            customer_data = consulta_receitafederal.get_data()
            cnpj = consulta_receitafederal.get_parsed()
        except Exception as error:
            logger.error(error)

        try:
            Customer.objects.get(cnpj=cnpj)
            creation_status = True
            logger.error('Customer already exists, creating the opportunity')
            return Response({'status': 'Customer already exists, creating the opportunity'}, 200)
        except Customer.DoesNotExist:
            logger.info('Customer doesnt exist, creating the customer')

            if customer_data['status'] != 'ERROR':
                logger.info(f'org data from receita: {customer_data}')
                customer = Customer.objects.create(razao_social=customer_data['nome'], telefone=customer_data['telefone'], email=customer_data['email'], bairro=customer_data['bairro'], logradouro=customer_data['logradouro'], numero=customer_data['numero'], cep=customer_data['cep'], municipio=customer_data['municipio'], nome_fantasia=customer_data['fantasia'], natureza_juridica=customer_data['natureza_juridica'], estado=customer_data['uf'], cnpj=cnpj, type='customer')
                customer.save()
                customer_id = customer.id
                creation_status = True
                logger.info('Customer Created!')
                return Response({'Status': 'Customer created, creating the opportunity request.'})
            creation_status = False
            return Response(customer_data)
        finally:
            if creation_status:
                logger.info('Creating the opportunity request')
                requester_organzation_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
                logger.info(f'requester org id: {requester_organzation_id}')
                requester_organization_instance = Customer.objects.get(id=requester_organzation_id)
                logger.info(f'requester org instance: {requester_organization_instance}')
                customer = Customer.objects.get(cnpj=cnpj)
                logger.info(f'getting the customer: {customer}')

                logger.info('Creating the opportunity...')
                opportunity = Opportunity.objects.create(opportunity_name=request.data['opportunity_name'], partner=requester_organization_instance, customer=customer, opportunity_description=request.data['description'], user=request.user)
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

            else: logger.error('Error in customer Get or Creation')

    def retrieve(self, request):
        organization = CustomerObject(request)
        opportunities = None
        if organization.get_customer_object().type == 'root':
            opportunities = Opportunity.objects.all()
            logger.info(opportunities)
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
            opportunity = Opportunity.objects.get(id=request.GET['opportunity_id'])

            if opportunity.partner.id == organization.get_customer_object().id or organization.get_customer_object().type == 'root':
                opportunity.resources = []
                resources = ResourceOfOpportunity.objects.filter(opportunity=opportunity)
                for resource in resources:
                    opportunity.resources.append(
                        {'resource_name': resource.resource.resource_name, 'resource_id': resource.resource.id})
                opportunity.history = []
                history = SalesRelatioshipFlow.objects.filter(customer=opportunity.customer, opportunity=opportunity)
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

class CustomerSalesHistory(viewsets.ViewSet):
    permission_classes = (IsPartner, )

    def create_customer_activity(self, request):
        organization = CustomerObject(request)

        try:
            opportunity = Opportunity.objects.get(id=request.data['opportunity_id'])
            partner = opportunity.partner.id
            if opportunity.partner.id == organization.get_customer_object().id or organization.get_customer_object().type == 'root':
                sales_activity = SalesRelatioshipFlow.objects.create(partner=partner, customer_id=request.data['customer_id'],
                                                                     opportunity_id=request.data['opportunity_id'], description=request.data['description'],
                                                                     author=request.user)
                sales_activity.save()
                serializer = HistorySerializer(sales_activity)
                return Response(serializer.data)
        except Opportunity.DoesNotExist:
            logger.error('Opportunity doesnt exist')
            return Response(messages.opportunity_doesnt_exist)

        except Exception as error:
            logger.error(error)

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

class CalculatorView(viewsets.ViewSet):
    # permission_classes = (IsRoot, )

    def calc(self, request):
        if 'compute' in request.data.keys():
            quotation = Calculator().calc_compute(request.data['compute']['mem'], request.data['compute']['cpu'])
            quotation = round(quotation, 2)
            serializer = ComputeQuotationSerializer(quotation)
            return Response(serializer.data)

        elif 'storage' in request.data.keys():
            if 'ssd' in request.data['storage']:
                ssd_quotation = Calculator().calc_ssd(request.data['storage']['ssd'])
                logger.info(round(ssd_quotation, 2))
            if 'hdd' in request.data['storage']:
                hdd_quotation = Calculator().calc_hdd(request.data['storage']['hdd'])
                logger.info(round(hdd_quotation, 2))
            if 'object_storage' in request.data['storage']:
                obj_storage_quotation = Calculator().calc_object_storage(request.data['storage']['object_storage'])
                logger.info(round(obj_storage_quotation, 2))