from django.contrib import admin
from .models import Resource, ResourcesType
# Register your models here.

admin.site.register(Resource)
admin.site.register(ResourcesType)