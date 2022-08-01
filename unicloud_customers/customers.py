from unicloud_customers.models import UserCustomer, Customer, CustomerRelationship
from logs.setup_log import logger

class CustomerObject:
    def __init__(self, request):
        self.request = request

    def get_customer_object(self):
        try:
            requester_organzation_id = UserCustomer.objects.get(user_id=self.request.user.id).customer_id
            return Customer.objects.get(id=requester_organzation_id)
        except Exception as error:
            logger.error(error)

class PartnerObject(CustomerObject):

    def get_customer_of_partner_list(self):
        try:
            partner = self.get_customer_object()
            relationship = CustomerRelationship.objects.filter(partner=partner)
            customers_ids = []
            for customer in relationship:
                customers_ids.append(customer.customer_id)
            customers = Customer.objects.filter(id__in=customers_ids)
            return customers
        except Exception as error:
            logger.error(error)
            pass