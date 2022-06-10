from django.db import models

# Create your models here.

class ZadaraPods(models.Model):
    name = models.CharField(max_length=250)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    url_base = models.CharField(max_length=500)
    pod_user = models.CharField(max_length=50)
    pod_password = models.CharField(max_length=150)
    domain_tenant = models.CharField(max_length=300, null=True, default=None)