from json import dumps
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from .utilities import validateCNPJ, validateCPF
from django.core.exceptions import ValidationError
from .models import BasicInfo, ContractualInfo
from .tables import ClienteBasicInfoTable

# Create your views here.
@login_required
def appMenu(request, *args, **kwargs):
    table = ClienteBasicInfoTable(BasicInfo.objects.all())
    template_name = 'client_app_menu.html'
    context = {'table' : table}

    if request.GET.get('search-id'):
        method = request.GET.get('search-method')
        searchid = request.GET.get('search-id')
        
        if method not in ["CPF", "CNPJ", "ID", "NOME"]:
            context.update({
                "ERROR" : 1,
                "ERROR_HEADER" : "CPF ou CNPJ Inválido.",
                "ERROR_MSG" : "O número informado não é um CPF ou CNPJ válido."
            })

            return render(request, template_name, context)

        if method == "CPF":
            queryset = BasicInfo.objects.filter(numero_documento_CPF = searchid).latest('id')
        elif method == "CNPJ":
            queryset = BasicInfo.objects.filter(numero_documento_CNPJ = searchid).latest('id')
        elif method == "id":
            queryset = BasicInfo.objects.get(id = searchid)
        elif method == "NOME":
            queryset = BasicInfo.objects.filter(nome = searchid).latest('id')
        
        if not queryset:
            context.update({
                "ERROR" : 1,
                "ERROR_HEADER" : "Cliente Não Encontrado.",
                "ERROR_MSG" : "A busca não retornou nenhum cliente. Verifique se o cliente está cadastrado, se não, cadastre-o."
            })

            return render(request, template_name, context)
        
        # Getting Alocated Employees Info
    
        contractualinfo = ContractualInfo.objects.filter(basicinfo_id = queryset.id)
        context.update({
            "SEARCH_OBJ" : queryset,
            "SEARCH_OBJ_EMPLOYEES" : contractualinfo
        })
            
    return render(request, template_name, context)

def autocompleteByname(request, *args, **kwargs):

    if request.is_ajax():
        term = request.GET.get('term', '')
        names = BasicInfo.objects.filter(nome__contains = term)[:20]

        print(term)

        results = []
        
        for name in names:
            name_json = {}
            
            name_json  = name.id
            name_json  = name.nome
            name_json  = name.nome

            

            results.append(name_json)
        
        data = dumps(results)
    
    else:
        data = 'fail'
    
    mimetype = 'application/json'

    print(data)

    return HttpResponse(data, mimetype)
