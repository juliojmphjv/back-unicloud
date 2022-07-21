from unicloud_customers.models import UserCustomer, Customer
class CustomerObject:
    def __init__(self, request):
        self.request = request

    def get_customer_object(self):
        requester_organzation_id = UserCustomer.objects.get(user_id=self.request.user.id).customer_id
        return Customer.objects.get(id=requester_organzation_id)