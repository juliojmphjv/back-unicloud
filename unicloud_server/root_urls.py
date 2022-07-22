from django.urls import path
from unicloud_sales.api.viewset import OpportunityStatus

urlpatterns = [
    path('opportunity-status/', OpportunityStatus.as_view({'patch': 'set_opportunity_status'})),
]