from django.contrib import admin
from .models import (
    BasicInfo,
    AddressInfo,
    ContractualInfo,
)
# Register your models here.
admin.site.register(BasicInfo)
admin.site.register(AddressInfo)
admin.site.register(ContractualInfo)