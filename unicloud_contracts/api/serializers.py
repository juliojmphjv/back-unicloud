from rest_framework import serializers

class ContractSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    term = serializers.IntegerField()  # Contract month period
    readjust_cycle = serializers.IntegerField()  # month
    amount = serializers.DecimalField(max_digits=19, decimal_places=10)
    note = serializers.CharField(max_length=100000)
    contract = serializers.CharField(max_length=300)