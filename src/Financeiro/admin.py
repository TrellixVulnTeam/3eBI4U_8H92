from django.contrib import admin
from .models import Entrada, Saida, Balanco, LancamentosFixos

# Register your models here.

admin.site.register(Entrada)
admin.site.register(Saida)
admin.site.register(Balanco)
admin.site.register(LancamentosFixos)