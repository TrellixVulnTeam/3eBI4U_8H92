from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from . import forms

from Cliente.models import ServiceOrder as OS

# Create your views here.

class GerarFatura(FormView):
    form_class = forms.ClienteListing
    template_name = 'gerar_fatura.html'
    

# API Views
def ListaOS(request, *args, **kwargs):
    cliente = request.GET.get('cliente')
    orders = OS.objects.filter(cliente = cliente).filter(faturado = False)

    data = {
        'OSList'    :   orders
        }

    return HttpResponse(render_to_string('lista_OS.html', data))

def GeraFatura(request, *args, **kwargs):
    order_ids = request.GET.get('orders')
    order_ids = [int(x) for x in order_ids.split(',')]

    orders  =   OS.objects.filter(id__in=order_ids)
    
    data    = {
        'orders'    :   orders,
        'date'      :   timezone.localdate(timezone.now())
    }

    return HttpResponse(render_to_string('fatura.html', data))