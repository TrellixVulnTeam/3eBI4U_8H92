from django.contrib import admin
from .models import (
    BasicInfo,
    AddressInfo,
    ContractualInfo,
    ServiceGround,
    ServiceDescription,
    ServiceOrder
)

# Register your models here.
admin.site.register(BasicInfo)
admin.site.register(AddressInfo)
admin.site.register(ContractualInfo)
admin.site.register(ServiceGround)
admin.site.register(ServiceDescription)
admin.site.register(ServiceOrder)