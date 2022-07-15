from django.db import models
from unicloud_contracts.models import Contracts
# Create your models here.

class ResourcesType(models.Model):
    resource_type = models.CharField(max_length=50)


class Resource(models.Model):
    resource_name = models.CharField(max_length=150)
    type = models.ForeignKey(ResourcesType, on_delete=models.CASCADE)

class assets(models.Model):
    contract = models.ForeignKey(Contracts, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.PROTECT)