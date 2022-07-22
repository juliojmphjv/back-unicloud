from django.urls import path
from unicloud_sales.api.viewset import OneOpportunity

urlpatterns = [
    path('get-one-opportunity/', OneOpportunity.as_view({'get': 'get_one_opportunity'})),
]