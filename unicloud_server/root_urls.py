from django.urls import path
from unicloud_sales.api.viewset import OpportunityStatus
from unicloud_dashboard.api.viewset import RootDashboard
from unicloud_customers.api.viewset import PartnerViewSet
urlpatterns = [
    path('partner/', PartnerViewSet.as_view({'post': 'create'})),
    path('opportunity-status/', OpportunityStatus.as_view({'patch': 'set_opportunity_status'})),
    path('dashboard/', RootDashboard.as_view({'get': 'get_dashboard'}))
]