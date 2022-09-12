from re import T
from unicodedata import name
from unicloud_sales.models import Opportunity, SalesRelatioshipFlow, ResourceOfOpportunity, SubscriptionsModel, CurrencyModel
from rest_framework import viewsets
from unicloud_customers.customer_permissions import IsPartner, IsRoot
from unicloud_customers.models import Customer, UserCustomer
from unicloud_customers.receita_federal import ConsultaReceita
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from logs.setup_log import logger
from unicloud_customers.customers import CustomerObject
from .serializers import OpportunitySerializer, OneOpportunitySerializer, ComputeQuotationSerializer, HistorySerializer, SubscriptionSerializer, CurrencySerializer, SetCurrencySerializer
from django.core import serializers
from error_messages import messages
from unicloud_customers.receita_federal import ConsultaReceita
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from ..calculator_tool import Calculator
import requests

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
        logger.info(cnpj)
        try:
            Customer.objects.get(cnpj=cnpj)
            creation_status = True
            logger.error('Customer already exists, creating the opportunity')
            return Response({'status': 'Customer already exists, creating the opportunity'}, 200)
        except Customer.DoesNotExist:
            logger.info('Customer doesnt exist, creating the customer')

            if customer_data['status'] != 'ERROR':
                logger.info(f'org data from receita: {customer_data}')
                customer = Customer.objects.create(razao_social=customer_data['nome'],\
                                                   telefone=customer_data['telefone'],\
                                                   email=customer_data['email'], \
                                                   bairro=customer_data['bairro'],\
                                                   logradouro=customer_data['logradouro'],\
                                                    numero=customer_data['numero'],\
                                                    cep=customer_data['cep'],\
                                                    municipio=customer_data['municipio'],\
                                                    nome_fantasia=customer_data['fantasia'],\
                                                    natureza_juridica=customer_data['natureza_juridica'],\
                                                    estado=customer_data['uf'],\
                                                    cnpj=cnpj,\
                                                    type='customer')
                customer.save()
                customer_id = customer.id
                creation_status = True
                logger.info('Customer Created!')
                return Response({'Status': 'Customer created, creating the opportunity request.'})
            creation_status = False
            return Response(customer_data)
        finally:
            if creation_status:
                opp = request.data['opportunity_name']
                try:
                    logger.info('Creating Opportunity')
                    requester_organzation_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
                    requester_organization_instance = Customer.objects.get(id=requester_organzation_id)
                    customer = Customer.objects.get(cnpj=cnpj)

                    opportunity = Opportunity.objects.create(opportunity_name=request.data['opportunity_name'],\
                                                             partner=requester_organization_instance,\
                                                             customer=customer,\
                                                             opportunity_description=request.data['description'],\
                                                             user=request.user)
                    opportunity.save()
                    logger.info('Opportunity request created.')
                except Exception as error:
                    logger.error(f"Error in Opportunity Creation - {error}")

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
                    activity = SalesRelatioshipFlow.objects.create(partner=requester_organization_instance,\
                                                                   customer=customer,\
                                                                   author=request.user,\
                                                                   description=f'{requester_organization_instance.razao_social} requesting an opportunity register to work with {opp} in {customer.razao_social}. Opportunity pending, waiting for the Sales team review.',
                                                                   opportunity=opportunity)
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
                sales_activity = SalesRelatioshipFlow.objects.create(partner_id=partner, customer_id=request.data['customer_id'],
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
    permission_classes = (IsRoot, )

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

class Subscriptions(viewsets.ViewSet):
    permission_classes = (IsRoot, )

    def create(self, request):
        
        try:
            subscription = SubscriptionsModel.objects.get(name=request.data['name'])
            logger.info('has!')
            return Response(messages.subscription_already_exists, 409)
        except SubscriptionsModel.DoesNotExist:
            logger.info("dont exists")
            new_subscription = SubscriptionsModel.objects.create(name=request.data['name'], months=request.data['months'], discount=request.data['discount'])
            new_subscription.save()
            logger.info("created")
            serializer = SubscriptionSerializer(new_subscription)
            logger.info("serialized")
            return Response(serializer.data)


    def update(self, request):
        logger.info(request.data)
        try:
            subscriptions = SubscriptionsModel.objects.get(id=request.data['subscription_id'])
            logger.info(subscriptions)
            if 'new_name' in request.data.keys():
                already_had_this_name = SubscriptionsModel.objects.filter(name=request.data['new_name']).exists()
                if already_had_this_name:
                    return Response(messages.already_existis_subscription_whith_this_name, 409)
                else:
                    subscriptions.name = request.data['new_name']
            if 'new_months_value' in request.data.keys():
                subscriptions.months = request.data['new_months_value']
                
            if 'new_discount_value' in request.data.keys():
                subscriptions.discount = request.data['new_discount_value']
            
            subscriptions.save()
            logger.info(subscriptions)
            serializer = SubscriptionSerializer(subscriptions)
            return Response(serializer.data)

        except SubscriptionsModel.DoesNotExist:
            return Response(messages.subscription_doesnt_existis)

        except Exception as error:
            logger.error(error)

        

    def retrieve(self, request):
        subscriptions = SubscriptionsModel.objects.all()
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)

    def delete(self, request):
        try:
            subscription = SubscriptionsModel.objects.get(id=request.data['subscription_id'])
            subscription.delete()
            return Response(messages.deleted, 200)
        except SubscriptionsModel.DoesNotExist:
            return Response(messages.subscription_doesnt_existis, 404)
        except Exception as error:
            logger.error(error)

class Measure(viewsets.ViewSet):
    permission_classes = (IsRoot, )

    def set_values(self, request):
        pass

class Currency(viewsets.ViewSet):
    permission_classes = (IsRoot, )

    def set_currency(self, request):
        try:
            currency = CurrencyModel.objects.get(currency=request.data['currency'])
            if 'currency_name' in request.data.keys():
                currency.currency = request.data['currency_name']
            if 'unicloud_dollar' in request.data.keys():
                currency.unicloud_dollar = request.data['unicloud_currency']
            if 'safety_margin' in request.data.keys():
                currency.safety_margin = request.data['safety_margin']

            currency.save()
            serializer = SetCurrencySerializer(currency)
            return Response(serializer.data)

        except CurrencyModel.DoesNotExist:
            logger.info("dont exists")
            try:
                new_currency = CurrencyModel.objects.create(currency=request.data['currency'], unicloud_dollar=request.data['unicloud_dollar'], safety_margin=request.data['safety_margin'])
                new_currency.save()
            except Exception as error:
                logger.error(error)
            logger.info("created")
            serializer = SetCurrencySerializer(new_currency)
            logger.info("serialized")
            return Response(serializer.data)

        except Exception as error:
            logger.error(error)

    def retrieve(self, request):
        try:
            currencies = CurrencyModel.objects.all()
            for currency in currencies:
                if currency.currency == 'usd':
                    req = requests.get("https://economia.awesomeapi.com.br/all/USD-BRL")
                    quotation = req.json()
                    currency.ptax = quotation["USD"]["bid"]
                    currency.overpriced_unicloud_currency =  currency.unicloud_currency+((currency.unicloud_currency/100)*15)
                else:
                    currency.ptax = 0
                    currency.overpriced_unicloud_currency = 0


            serializer = CurrencySerializer(currencies, many=True)
            return Response(serializer.data)
        except Exception as error:
            return Response({"Error": "Error"})

    def delete(self, request):
        try:
            currency = CurrencyModel.objects.get(id=request.data['currency_id'])
            currency.delete()
            return Response(messages.deleted, 200)
        except Exception as error:
            logger.error(error)