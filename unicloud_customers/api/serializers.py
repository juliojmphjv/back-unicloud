from rest_framework import serializers
from rest_framework.serializers import Serializer, FileField


class CustomerSerializer(serializers.Serializer):
     id = serializers.IntegerField()
     razao_social = serializers.CharField(max_length=250)
     telefone = serializers.CharField(max_length=300)
     email = serializers.EmailField()
     bairro = serializers.CharField(max_length=250)
     logradouro = serializers.CharField(max_length=250)
     numero = serializers.CharField(max_length=200)
     cep = serializers.CharField(max_length=15)
     municipio = serializers.CharField(max_length=100)
     nome_fantasia = serializers.CharField(max_length=250)
     natureza_juridica = serializers.CharField(max_length=250)
     estado = serializers.CharField(max_length=250)
     cnpj = serializers.CharField(max_length=25)
     type = serializers.CharField(max_length=50)
     is_active = serializers.BooleanField()

class CustomerTypeSerializer(serializers.Serializer):
     type = serializers.CharField(max_length=15)

class LogoSerializer(serializers.Serializer):
    logo = FileField()
