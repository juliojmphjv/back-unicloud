from django.contrib import admin
from .models import Opportunity, ResourceOfOpportunity, SalesRelatioshipFlow
# Register your models here.
admin.site.register(Opportunity)
admin.site.register(ResourceOfOpportunity)
admin.site.register(SalesRelatioshipFlow)