from django.contrib import admin
from .models import Customer, CustomerRelationship, UserCustomer, InvitedUser
# Register your models here.
admin.site.register(Customer)
admin.site.register(CustomerRelationship)
admin.site.register(UserCustomer)
admin.site.register(InvitedUser)