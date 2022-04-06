from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    razao_social = models.CharField(max_length=250)
    telefone = models.CharField(max_length=300, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    bairro = models.CharField(max_length=250, blank=True, null=True)
    logradouro = models.CharField(max_length=250, blank=True, null=True)
    numero = models.CharField(max_length=200, blank=True, null=True)
    cep = models.CharField(max_length=15, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    nome_fantasia = models.CharField(max_length=250, null=True)
    natureza_juridica = models.CharField(max_length=250, blank=True, null=True)
    estado = models.CharField(max_length=250, blank=True, null=True)
    cnpj = models.CharField(max_length=25, null=True)
    criado_em = models.DateField(auto_created=True, null=True, blank=True)
    type = models.CharField(max_length=50)

class UserCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class CustomerRelationship(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='customer')
    partner = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='partner')

class InvitedUser(models.Model):
    email = models.EmailField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    token = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
