from django.db import models
from unicloud_customers.models import Customer
from django.contrib.auth.models import User
from unicloud_resources.models import Resource

# Create your models here.
class Opportunity(models.Model):
    partner = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales_partner_opportunity_requester')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales_customer_opportunity')
    opportunity_description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_user_requester')
    status = models.CharField(max_length=50, default='opportunity_pending')
    request_date = models.DateTimeField(auto_now_add=True)

class ResourceOfOpportunity(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT, related_name='resource_of_sales_opportunity')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.PROTECT, related_name='the_sales_opportunity')

class SalesRelatioshipFlow(models.Model):
    partner = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='partner_sales')
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='customer_to_sale')
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_author')
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
