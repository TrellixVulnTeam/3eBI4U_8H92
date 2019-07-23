from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.BasicInfo)
admin.site.register(models.AddressInfo)
admin.site.register(models.ContractualInfo)
admin.site.register(models.ServiceGround)
admin.site.register(models.ServiceDescription)
admin.site.register(models.ServiceOrder)
admin.site.register(models.ServiceRecord)
admin.site.register(models.OccurrenceCall)