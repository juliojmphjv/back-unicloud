from django.urls import path
from unicloud_sales.api.viewset import OpportunityStatus
from unicloud_dashboard.api.viewset import RootDashboard

urlpatterns = [
    path('opportunity-status/', OpportunityStatus.as_view({'patch': 'set_opportunity_status'})),
    path('dashboard/', RootDashboard.as_view({'get': 'get_dashboard'}))
]