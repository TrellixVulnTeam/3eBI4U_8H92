from django.db import models
from Cliente.models import BasicInfo as Cliente, ServiceOrder as OS

# Create your models here.
class Fatura(models.Model):
    # Primary Key
    id = models.AutoField(primary_key = True)

    # Foreign Keys
    cliente     =   models.ForeignKey(Cliente, models.CASCADE, 'fatura_cliente', null = True, blank = True)
    OS          =   models.ForeignKey(OS, models.CASCADE, 'fatura_OS', null = True, blank = True)
    
    # Model Main Fields
    valor_total         =   models.DecimalField(decimal_places = 2, max_digits = 12, null = True, blank = True)
    deconto             =   models.DecimalField(decimal_places = 2, max_digits = 4, null = True, blank = True)
    pagamento_efetuado  =   models.BooleanField(default = False)
    data_emissao        =   models.DateField(auto_now_add = True)
    data_vencimento     =   models.DateField(null = True, blank = True)
    data_pagamento      =   models.DateField(null = True, blank = True)