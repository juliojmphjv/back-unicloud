from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from ..models import InvitedUser, Customer, UserCustomer, CustomerRelationship
from .serializers import CustomerSerializer, CustomerTypeSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from ..receita_federal import ConsultaReceita
from rest_framework.decorators import action, permission_classes
from error_messages import messages
from rest_framework.renderers import JSONRenderer
from django.template.loader import get_template
from unicloud_tokengenerator.generator import TokenGenerator
from unicloud_mailersystem.mailer import UniCloudMailer
from django.shortcuts import get_object_or_404
from check_root.unicloud_check_root import CheckRoot

class CustomerViewSet(viewsets.ViewSet):
    permission_classes(IsAuthenticated,)
    def create(self, request):
        response = None
        status = None
        consulta = ConsultaReceita(request.data['cnpj'])
        customer_data = consulta.get_data()
        check_root = CheckRoot(request)
        organzation_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        organization_instance = Customer.objects.get(id=organzation_id)
        if check_root.is_root():
            customer, created = Customer.objects.get_or_create(razao_social=customer_data['nome'], telefone=customer_data['telefone'], email=customer_data['email'], bairro=customer_data['bairro'], logradouro=customer_data['logradouro'], numero=customer_data['numero'], cep=customer_data['cep'], municipio=customer_data['municipio'], nome_fantasia=customer_data['fantasia'], natureza_juridica=customer_data['natureza_juridica'], estado=customer_data['uf'], cnpj=customer_data['cnpj'], type=request.data['type'])
        else:
            customer, created = Customer.objects.get_or_create(razao_social=customer_data['nome'], telefone=customer_data['telefone'], email=customer_data['email'], bairro=customer_data['bairro'], logradouro=customer_data['logradouro'], numero=customer_data['numero'], cep=customer_data['cep'], municipio=customer_data['municipio'], nome_fantasia=customer_data['fantasia'], natureza_juridica=customer_data['natureza_juridica'], estado=customer_data['uf'], cnpj=customer_data['cnpj'], type='customer')
        if created:
            relationship = CustomerRelationship(customer=customer, partner=organization_instance)
            relationship.save()
            token_generator = TokenGenerator(request.data['email'])
            token = token_generator.gettoken()
            invited_user, created = InvitedUser.objects.get_or_create(email=request.data['email'],customer=customer, token=token)
            if created:
                mensagem = {
                    'empresa': customer.razao_social,
                    'link': f'http://127.0.0.1:3000/auth-register/?token={token}'
                }
                rendered_email = get_template('email/welcome.html').render(mensagem)
                mailer = UniCloudMailer(request.data['email'], 'Bem vindo ao Uni.Cloud Broker', rendered_email)
                mailer.send_mail()
                response = CustomerSerializer(customer)
                status = 200
                return Response(response.data, status)
            return Response(response, status)
        if not created:
            response = messages.already_exist
            status = 400
            return Response(response, status)
        response = CustomerSerializer(customer)
        status = 200
        return Response(response.data, status)


    def list(self, request):
        organization = Customer.objects.get(id=UserCustomer.objects.get(user_id=request.user.id).customer_id)
        customers = []
        customer_list = CustomerRelationship.objects.filter(partner_id=organization.id)
        for customer in customer_list:
            customers.append(customer.customer_id)
        customerlist = Customer.objects.filter(id__in=customers)

        serializer = CustomerSerializer(customerlist, many=True)
        return Response(serializer.data)

class OneCustomerViewSet(viewsets.ViewSet):
    permission_classes(IsAuthenticated,)
    def partial_update(self, request, pk):
        if request.user.is_superuser and request.user.is_staff and request.user.is_authenticated:
            customer = Customer.objects.filter(pk=pk)
            customer.update(**request.data)
            serializer = CustomerSerializer(customer, many=True)
            return Response(serializer.data)

class CustomerType(viewsets.ViewSet):
    permission_classes(IsAuthenticated,)
    def get_type(self, request):
        customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerTypeSerializer(customer)
        return Response(serializer.data)

class Organization(viewsets.ViewSet):
    permission_classes(IsAuthenticated,)

    def get_organization(self, request):
        customer_id = UserCustomer.objects.get(user_id=request.user.id).customer_id
        customer = Customer.objects.get(id=customer_id)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)