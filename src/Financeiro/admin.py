from django.contrib import admin
from .models import Entrada, Saida, Balanco, LancamentosFixos, EntradaProd, SaidaProd

# Register your models here.

admin.site.register(Entrada)
admin.site.register(Saida)
admin.site.register(Balanco)
admin.site.register(LancamentosFixos)
admin.site.register(EntradaProd)
admin.site.register(SaidaProd)