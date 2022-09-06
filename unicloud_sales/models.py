from operator import mod
from pyexpat import model
from unicodedata import name
from django.db import models
from unicloud_customers.models import Customer
from django.contrib.auth.models import User
from unicloud_resources.models import Resource
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

# Create your models here.
class Opportunity(models.Model):
    opportunity_name = models.CharField(max_length=300, null=True, default=None)
    partner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales_partner_opportunity_requester')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales_customer_opportunity')
    opportunity_description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_user_requester')
    status = models.CharField(max_length=50, default='opportunity_pending')
    request_date = models.DateTimeField(auto_now_add=True)

    def natural_key(self):
        return (self.opportunity_name)

class ResourceOfOpportunity(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT, related_name='resource_of_sales_opportunity')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.PROTECT, related_name='the_sales_opportunity')

class SalesRelatioshipFlow(models.Model):
    partner = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='partner_sales')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='customer_to_sale')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_author')
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    opportunity = models.ForeignKey(Opportunity, null=True, on_delete=models.CASCADE, related_name='opportunity_of_activity')

    def natural_key(self):
        return (self.author.username)

class SubscriptionsModel(models.Model):
    name = models.CharField(max_length=100)
    months = models.IntegerField()
    discount = models.FloatField()

class MeasureModel(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]    
class CurrencyModel(models.Model):
    currency = models.CharField(max_length=5, default='usd')
    unicloud_dollar = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    safety_margin = models.DecimalField(max_digits=3, decimal_places=0, default=Decimal(0), validators=PERCENTAGE_VALIDATOR)
