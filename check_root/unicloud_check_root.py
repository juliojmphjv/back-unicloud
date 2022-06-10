from unicloud_customers.models import Customer, UserCustomer
from logs.setup_log import logger

class CheckRoot:
    def __init__(self, request):
        self.request=request
        self.user_customer_instance = UserCustomer

    def is_root(self):
        organization = Customer.objects.get(id=self.user_customer_instance.objects.get(user_id=self.request.user.id).customer_id)
        logger.info(f'user is staff: {self.request.user.is_staff}')
        logger.info(f'user is superuser: {self.request.user.is_superuser}')
        logger.info(f'customer type is : {organization.type}')

        if self.request.user.is_staff and self.request.user.is_superuser and organization.type == "root":
            return True
        return False

