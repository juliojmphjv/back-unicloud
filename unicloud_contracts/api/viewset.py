from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Contracts, Intermediary, Contractor, CustomerContracts
from unicloud_customers.models import Customer
from logs.setup_log import logger
from .serializers import ContractSerializer
from rest_framework.response import Response

class ContractsViewSet(viewsets.ViewSet):
    permission_classes = (IsAdminUser,)

    def create(self, request):
        try:
            contract = Contracts.objects.create(name=request.data['name'], start_date=request.data['start_date'], end_date=request.data['end_date'], term=request.data['term'], readjust_cycle=request.data['readjust_cycle'], amount=request.data['amount'], note=request.data['note'])
            contract.save()
            customer = Customer.objects.get(id=request.data['customer_id'])
            if request.data['intermediary']:
                intermediary = Intermediary.objects.create(intermediary=request.data['intermediary'], contract=contract)
                intermediary.save()
            contractor = Contractor.objects.create(contractor=customer, contract=contract)
            contractor.save()
            customer_contract_relationship = CustomerContracts.objects.create(customer=customer, contract=contract)
            customer_contract_relationship.save()
            serializer = ContractSerializer(contract)
            return Response(serializer.data)

        except Exception as error:
            logger.error(error)