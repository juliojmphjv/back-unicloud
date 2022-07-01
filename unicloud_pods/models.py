from django.db import models

# Create your models here.

class ZadaraPods(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    url_base = models.CharField(max_length=500)
    pod_user = models.CharField(max_length=50, null=True)
    pod_password = models.CharField(max_length=150, null=True)
    domain_tenant = models.CharField(max_length=300, null=True)
    spare_nodes = models.IntegerField(default=0)
    project_id = models.CharField(max_length=50, default=None, null=True, blank=True)