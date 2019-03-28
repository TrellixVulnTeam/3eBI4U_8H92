from django.contrib import admin
from .models import (
    BasicInfo,
    AddressInfo,
    DocumentsInfo,
    ContactInfo,
    ForeignerInfo,
    HandicappedInfo,
    BankingInfo,
    AnotherJobInfo,
    InternInfo,
    PositionInfo,
    ContractualInfo,
    DocumentAttachments,
    Dependente
)
# Register your models here.
admin.site.register(Dependente)
admin.site.register(BasicInfo)
admin.site.register(AddressInfo)
admin.site.register(DocumentsInfo)
admin.site.register(ContactInfo)
admin.site.register(ForeignerInfo)
admin.site.register(HandicappedInfo)
admin.site.register(BankingInfo)
admin.site.register(AnotherJobInfo)
admin.site.register(InternInfo)
admin.site.register(PositionInfo)
admin.site.register(ContractualInfo)
admin.site.register(DocumentAttachments)
