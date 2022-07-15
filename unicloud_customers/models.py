from django.db import models
from django.contrib.auth.models import User
from unicloud_server.custom_azure import AzureMediaStorage
from unicloud_contracts.models import Contracts
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
    cnpj = models.CharField(max_length=25)
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    type = models.CharField(max_length=50)
    is_active = models.BooleanField(null=True, default=True, auto_created=True)

    def __str__(self):
        return self.razao_social

class UserCustomer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    def __str__(self):
        return f'{self.user} - {self.customer}'

class CustomerRelationship(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='customer')
    partner = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='partner')

    def __str__(self):
        return f'{self.customer} is a customer of {self.partner}'

class InvitedUser(models.Model):
    email = models.EmailField(primary_key=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    token = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.email} invitation from {self.customer}'

def customer_directory_path(instance, filename):
    return '{0}/{1}'.format(instance, filename)

class OrganizationLogo(models.Model):

    organization = models.ForeignKey(Customer, on_delete=models.CASCADE)
    logo = models.ImageField(storage=AzureMediaStorage, upload_to=customer_directory_path)

    def __str__(self):
        return self.organization.razao_social

class CustomerContracts(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    contract = models.ForeignKey(Contracts, on_delete=models.PROTECT)