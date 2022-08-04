from rest_framework.permissions import BasePermission
from logs.setup_log import logger
from unicloud_customers.models import Customer, UserCustomer

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user and request.user.is_authenticated:
                user_customer = UserCustomer.objects.get(user_id=request.user.id)
                customer = Customer.objects.get(id=user_customer.customer_id)
                return True if customer.type == 'partner' or customer.type == 'root' or customer.type == 'customer' else False
        except Exception as error:
            logger.error(error)
            return False

class IsPartner(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user and request.user.is_authenticated:
                user_customer = UserCustomer.objects.get(user_id=request.user.id)
                customer = Customer.objects.get(id=user_customer.customer_id)
                return True if customer.type == 'partner' or customer.type == 'root' else False
        except Exception as error:
            logger.error(error)
            return False

class IsRoot(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user and request.user.is_authenticated:
                user_customer = UserCustomer.objects.get(user_id=request.user.id)
                customer = Customer.objects.get(id=user_customer.customer_id)
                return True if customer.type == 'root' else False
        except Exception as error:
            logger.error(error)
            return False

class AllowAny(BasePermission):
    def has_permission(self, request, view):
        return True