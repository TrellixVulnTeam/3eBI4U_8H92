from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, HttpResponse, redirect, render_to_response
from django.template.loader import render_to_string
from django.utils import timezone
from . import models
from . import forms
from Cliente.models import BasicInfo as Cliente, ServiceOrder as OS
from Notificacao.views import notify
import json
import decimal

# Utility Class for Pagination
class Pagination():
    def __init__(self, full_query, paginate_by):
        self.full_query = full_query
        self.paginate_by = paginate_by
    
    def get_pagination(self):
        return [self.full_query[x : x + self.paginate_by] for x in range(0, len(self.full_query), self.paginate_by)]
        
    def is_paginated(self):
        return(len(self.get_pagination()) > 1)

    def total_pages(self):
        return len(self.get_pagination())
    
    def get_page(self, page):
        return self.get_pagination()[page]

    def pages(self):
        return range(1, len(self.get_pagination()) + 1)

# Class Based Views
class financeiroMenu(View):
    template_name = 'menu.html'
    context = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)

class FaturaOSSelectionView(View):
    template_name = 'fatura/fatura_selectOS.html'
    context = {}

    def get(self, request, *args, **kwargs):

        form = forms.ClienteListing()

        self.context.update({
            'form' : form
        })

        return render(request, self.template_name, self.context)

class FaturaCreationView(View):
    template_name = 'fatura/fatura_create.html'
    context = {}
    def get(self, request, *args, **kwargs):
        os_str = self.kwargs.pop('os')
        OSList = OS.objects.filter(id__in = [int(x) for x in os_str[6:].split('&order=')]).order_by('-id')

        for order in OSList:
            if order.faturado == True:
                messages.error(request, 'OS #{} já faturada.'.format(order.OS))
                return redirect('financeiro/fatura/selecionarOS', permanent = True)

        self.context.update({
            'OSList' : OSList
        })


        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        OSList = json.loads(request.POST.get('OS'))
        OSList = [OS.objects.get(id = order) for order in OSList]
        total = decimal.Decimal(request.POST.get('total'))
        discount = decimal.Decimal(request.POST.get('discount'))

        fatura = models.Fatura.objects.create(cliente = OSList[0].cliente, valor_total = total, desconto = discount)
        
        for order in OSList:
            order.fatura = fatura
            order.faturado = True
            order.save()
        messages.success(request, 'Fatura #{} gerada com sucesso !'.format(fatura.NumeroFatura))

        return redirect(request.META.get('HTTP_REFERER', '/'), permanent = True)

# API Views
def listaClientes(request, *args, **kwargs):
    
    if not request.is_ajax():
        raise TypeError('Request Must Be AJAX.')
    
    # Constant values
    template_name = 'fatura/OS_list.html'
    paginate_by = 3

    # Getting AJAX parameters and Obtaining Objects (If Needed)
    cliente = models.Cliente.objects.get(id = request.GET.get('cliente'))
    page = int(request.GET.get('page'))

    # Querying DB 
    fullOS = cliente.ordem_servico_cliente.filter(faturado = False).order_by('-id') 

    # Processing Values
    pagination = Pagination(fullOS, paginate_by)
    current_page = pagination.get_page(page)

    # Generating Context Dict
    context = {
        'OSList' : fullOS,
        'pagination' : pagination,
        'current_page' : current_page,
        'current_page_number' : page
    }

    return HttpResponse(render_to_string(template_name, context))

    