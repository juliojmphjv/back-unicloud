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
from unicloud_users.api.viewsets import MyTokenObtainPairView, UsersViewSet, RegisterViewSet, MenuViewSet, InvitedUsersViewSet, TokenViewSet
from unicloud_customers.api.viewset import CustomerViewSet, OneCustomerViewSet, CustomerType, Organization, OrganizationLogo, OrganizationLogoViewSet
from unicloud_dashboard.api.viewset import Dashboard
from unicloud_pods.api.viewset import ZadaraPodsViewSet
from django.conf.urls.static import static
from django.conf import settings


router = routers.DefaultRouter()
# router.register(r'users', Users)
# router.register(r'invited-user', InvitedUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('invited-user/', InvitedUsersViewSet.as_view({'post': 'create', 'get':'retrieve'}), name='invited-user'),
    path('token/', TokenViewSet.as_view({'post': 'check_token'}), name='token'),
    path('customers/', CustomerViewSet.as_view({'post': 'create', 'get': 'list'}), name='customers'),
    path('one-customer/<int:pk>/', OneCustomerViewSet.as_view({'patch': 'partial_update'})),
    path('register/', RegisterViewSet.as_view({'post': 'create'})),
    path('menu/', MenuViewSet.as_view({'get': 'retrieve'})),
    path('users/', UsersViewSet.as_view({'get': 'retrieve', 'post':'create'})),
    path('customer-type/', CustomerType.as_view({'get': 'get_type'})),
    path('get-organization/', Organization.as_view({'get': 'get_organization'})),
    path('organization-logo/', OrganizationLogoViewSet.as_view({'post': 'create', 'get': 'get_logo'})),
    path('create-zadara-pod/', ZadaraPodsViewSet.as_view({'post': 'create'})),
    path('dashboard/', Dashboard.as_view({'get': 'get_dashboard'}))
]
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

