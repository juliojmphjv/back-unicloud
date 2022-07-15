from django.db import models
from unicloud_customers.models import Customer
from unicloud_server.custom_azure import AzureContractsStorage
# Create your models here.

def customer_directory_path(instance, filename):
    return '{0}/{1}'.format(instance, filename)

class Contracts(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    term = models.IntegerField() #Contract month period
    readjust_cycle = models.IntegerField() #month
    amount = models.DecimalField(max_digits=19, decimal_places=10)
    note = models.TextField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    intermediary = models.ForeignKey(Customer, on_delete=models.CASCADE)
    contract = models.FileField(storage=AzureContractsStorage, upload_to=customer_directory_path)

