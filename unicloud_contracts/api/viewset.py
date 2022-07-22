from rest_framework import viewsets
from unicloud_customers.customer_permissions import IsRoot
from ..models import Contracts, Intermediary, ContractParty
from unicloud_customers.models import Customer
from logs.setup_log import logger
from .serializers import ContractSerializer
from rest_framework.response import Response
from rest_framework.decorators import permission_classes

class ContractsViewSet(viewsets.ViewSet):
    permission_classes = (IsRoot, )

    def create(self, request):
        try:
            contract = Contracts.objects.create(name=request.data['name'], start_date=request.data['start_date'], end_date=request.data['end_date'], term=request.data['term'], readjust_cycle=request.data['readjust_cycle'], amount=request.data['amount'], note=request.data['note'], contract=request.FILES.get('file_uploaded'))
            contract.save()
            contractor = Customer.objects.get(id=request.data['customer_id'])
            hired = Customer.objects.get(id=request.data['partner_id'])
            try:
                if request.data['intermediary']:
                    intermediary = Intermediary.objects.create(intermediary=request.data['intermediary'], contract=contract)
                    intermediary.save()
            except Exception as error:
                pass

            contract_parties = ContractParty.objects.create(contractor=contractor, hired=hired, contract=contract)
            contract_parties.save()

            serializer = ContractSerializer(contract)
            return Response(serializer.data)

        except Exception as error:
            logger.error(error)

    def retrieve(self, request):
        try:
            contracts = Contracts.objects.all()
            serializer = ContractSerializer(contracts, many=True)
            return Response(serializer.data)
        except Exception as error:
            logger.error(error)
            return Response({'error': error})

    def delete(self, request):
        try:
            contract = Contracts.objects.get(id=request.data['contract_id'])
            contract.delete()
            return Response({'status': 'deleted'})
        except Exception as error:
            logger.error(error)
            return Response({'error': error})