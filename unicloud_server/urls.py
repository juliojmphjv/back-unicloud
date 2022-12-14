"""unicloud_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import routers
from unicloud_users.api.viewsets import MyTokenObtainPairView, UsersViewSet, MenuViewSet, InviteUsersViewSet, TokenViewSet, UserRegisterViewSet, LoginV2, Indentify, UserPreference
from unicloud_customers.api.viewset import CustomerViewSet, OneCustomerViewSet, CustomerType, Organization, OrganizationLogoViewSet
from unicloud_dashboard.api.viewset import CustomerDashboard
from unicloud_pods.api.viewset import ZadaraPodsViewSet
from django.conf.urls.static import static
from django.conf import settings
from unicloud_resources.api.viewset import ResourceViewSet, ResourceTypeViewSet, AssetsViewSet
from unicloud_contracts.api.viewset import ContractsViewSet
from unicloud_sales.api.viewset import OpportunityRegister


router = routers.DefaultRouter()
# router.register(r'users', Users)
# router.register(r'invited-user', InvitedUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login-v2/', LoginV2.as_view({'post': 'login'}), name='login-v2'),
    path('indetify/', Indentify.as_view({'post': 'identify'}), name='identify'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('invite-user/', InviteUsersViewSet.as_view({'post': 'create', 'get': 'retrieve'}), name='invited-user'),
    path('check-token/', TokenViewSet.as_view({'post': 'check_token'}), name='token'),
    path('customers/', CustomerViewSet.as_view({'get': 'list'}), name='customers'),
    path('one-customer/<int:pk>/', OneCustomerViewSet.as_view({'patch': 'partial_update'})),
    path('menu/', MenuViewSet.as_view({'get': 'retrieve'})),
    path('users/', UsersViewSet.as_view({'get': 'retrieve'})),
    path('user-register/', UserRegisterViewSet.as_view({'post': 'user_register'})),
    path('customer-type/', CustomerType.as_view({'get': 'get_type'})),
    path('get-organization/', Organization.as_view({'get': 'get_organization'})),
    path('organization-logo/', OrganizationLogoViewSet.as_view({'post': 'create', 'get': 'get_logo'})),
    path('create-zadara-pod/', ZadaraPodsViewSet.as_view({'post': 'create'})),
    path('pods/', ZadaraPodsViewSet.as_view({'get': 'retrieve_list'})),
    path('dashboard/', CustomerDashboard.as_view({'get': 'get_dashboard'})),
    path('update-invitation/', TokenViewSet.as_view({'patch': 'update_invitation'})),
    path('resources/', ResourceViewSet.as_view({'post': 'create', 'get': 'retrieve', 'delete': 'delete', 'patch': 'update'})),
    path('resources-type/', ResourceTypeViewSet.as_view({'post': 'create', 'get': 'retrieve', 'patch': 'update'})),
    path('contracts/', ContractsViewSet.as_view({'post': 'create', 'get': 'retrieve', 'delete': 'delete'})),
    path('assets/', AssetsViewSet.as_view({'post': 'create', 'get': 'retrieve'})),
    path('opportunity-register/', OpportunityRegister.as_view({'post': 'create', 'get': 'retrieve'})),
    path('user-preferences/', UserPreference.as_view({'post': 'create', 'get': 'retrieve'})),

 
    #Root Routes.
    path('root/', include('unicloud_server.root_urls')),

    #Partners Routes
    path('partner/', include('unicloud_server.partner_urls')),

]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

