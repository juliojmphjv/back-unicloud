
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'brokermediastorage' # Must be replaced by your <storage_account_name>
    account_key = 'gxXiOCisdOZ8NaH8FW9ZDmJdbJfDMVjM0j9X/9+BlmHcG4AhJkx3wvsZiaSmDlAmPtizQnkMp9Xs/69TVQ9PDA==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'brokermediastorage' # Must be replaced by your storage_account_name
    account_key = 'gxXiOCisdOZ8NaH8FW9ZDmJdbJfDMVjM0j9X/9+BlmHcG4AhJkx3wvsZiaSmDlAmPtizQnkMp9Xs/69TVQ9PDA==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
