from django.urls import path
from unicloud_sales.api.viewset import OpportunityStatus, CalculatorView, Subscriptions, Currency
from unicloud_dashboard.api.viewset import RootDashboard
from unicloud_customers.api.viewset import PartnerViewSet

urlpatterns = [
    path('partner/', PartnerViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('opportunity-status/', OpportunityStatus.as_view({'patch': 'set_opportunity_status'})),
    path('dashboard/', RootDashboard.as_view({'get': 'get_dashboard'})),
    path('calculator/', CalculatorView.as_view({'post': 'calc'})),
    path('subscriptions/', Subscriptions.as_view({'post': 'create', 'get': 'retrieve', 'patch': 'update', 'delete': 'delete'})),
    path('currency/', Currency.as_view({'post': 'set_currency', 'get': 'retrieve'}))
]