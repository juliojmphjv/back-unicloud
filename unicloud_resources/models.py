from django.db import models
from unicloud_contracts.models import Contracts
# Create your models here.

class ResourcesType(models.Model):
    resource_type = models.CharField(max_length=50)

    def __str__(self):
        return self.resource_type


class Resource(models.Model):
    resource_name = models.CharField(max_length=150)
    monthly_houer = models.IntegerField(auto_created=True, default=730)
    unit_type = models.CharField(max_length=150, default='GB')
    type = models.ForeignKey(ResourcesType, on_delete=models.CASCADE)

    def __str__(self):
        return self.resource_name
    def natural_key(self):
        return (self.resource_name)

class Assets(models.Model):
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)
    qty = models.IntegerField(default=None, null=True, blank=True)