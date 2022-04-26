from unicloud_customers.models import Customer, UserCustomer
from logs.setup_log import logger

class CheckRoot:
    def __init__(self, request):
        logger.info("Check Root instantiated")
        self.__request=request
        self.__user_customer_instance = UserCustomer

    def is_root(self):
        logger.info("Customer Query")
        organization = Customer.objects.get(id=self.__user_customer_instance.objects.get(user_id=self.__request.user.id).customer_id)
        logger.info(organization)
        if self.__request.user.is_staff and self.__request.user.is_superuser and organization.type == "root" and organization.razao_social == "Uni.Cloud" :
            logger.info("is root!")
            return True
        logger.info("is not a root")
        return False

