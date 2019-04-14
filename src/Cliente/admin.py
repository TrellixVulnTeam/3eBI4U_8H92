from django.contrib import admin
from .models import (
    BasicInfo,
    AddressInfo,
    DocumentsInfo,
    ContactInfo,
    BankingInfo,
    ContractualInfo,
    DocumentAttachments,
)
# Register your models here.
admin.site.register(BasicInfo)
admin.site.register(AddressInfo)
admin.site.register(DocumentsInfo)
admin.site.register(ContactInfo)
admin.site.register(BankingInfo)
admin.site.register(ContractualInfo)
admin.site.register(DocumentAttachments)
