from django.urls import path
from unicloud_sales.api.viewset import OneOpportunity
from unicloud_dashboard.api.viewset import PartnerDashboard

urlpatterns = [
    path('get-one-opportunity/', OneOpportunity.as_view({'get': 'get_one_opportunity'})),
    path('dashboard/', PartnerDashboard.as_view({'get': 'get_dashboard'})),
]