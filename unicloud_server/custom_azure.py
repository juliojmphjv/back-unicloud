from storages.backends.azure_storage import AzureStorage
from django.conf import settings

class AzureMediaStorage(AzureStorage):
    account_name = 'brokermediastorage' # Must be replaced by your <storage_account_name>
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'brokermediastorage' # Must be replaced by your storage_account_name
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = 'static'
    expiration_secs = None

class AzureContractsStorage(AzureStorage):
    account_name = 'brokermediastorage'  # Must be replaced by your storage_account_name
    account_key = settings.AZURE_ACCOUNT_KEY
    azure_container = 'contracts'
    expiration_secs = 1800