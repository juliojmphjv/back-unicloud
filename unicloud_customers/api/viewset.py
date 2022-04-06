from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from ..models import InvitedUser, Customer
from .serializers import InvitedUserSerializer, CustomerSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from ..receita_federal import ConsultaReceita

class InvitedUserViewSet(viewsets.ViewSet):

    def create(self, request):
        customer = Customer.objects.get(id=1)
        inviteduser = InvitedUser(token=request.POST['token'], email=request.POST['email'], customer=customer)
        inviteduser.save()
        serializer = InvitedUserSerializer({'teste': 'teste'})
        return Response(serializer.data)

class CustomerViewSet(viewsets.ViewSet):

    def create(self, request):
        consulta = ConsultaReceita(request.POST['cnpj'])
        customer_data = consulta.get_data()
        customer = Customer(razao_social=customer_data['nome'], telefone=customer_data['telefone'], email=customer_data['email'], bairro=customer_data['bairro'], logradouro=customer_data['logradouro'], numero=customer_data['numero'], cep=customer_data['cep'], municipio=customer_data['municipio'], nome_fantasia=customer_data['fantasia'], natureza_juridica=customer_data['natureza_juridica'], estado=customer_data['uf'], cnpj=customer_data['cnpj'], type='customer')
        customer.save()
        serializer = CustomerSerializer({'teste':'teste'})
        return Response(serializer.data)