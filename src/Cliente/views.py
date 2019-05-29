from django.shortcuts import render
from .utilities import validateCNPJ, validateCPF
from django.core.exceptions import ValidationError
from .models import BasicInfo, ContactInfo, ContractualInfo


# Create your views here.
def appMenu(request, *args, **kwargs):
    template_name = 'client_app_menu.html'
    context = {}

    if request.GET.get('search-id'):
        searchid = request.GET.get('search-id')
        if '.' in searchid:
            try:
                validateCNPJ(searchid.replace('.','').replace('-','').replace('/',''))
                method = "CNPJ"
            except ValidationError:
                try:
                    validateCPF(searchid.replace('.','').replace('-','').replace('/',''))
                    method = "CPF"
                except ValidationError:
                    method = "Invalid"
        else:
            method = "id"
        
        if method == "Invalid":
            context = {
                "ERROR" : 1,
                "ERROR_HEADER" : "CPF ou CNPJ Inválido.",
                "ERROR_MSG" : "O número informado não é um CPF ou CNPJ válido."
            }

            return render(request, template_name, context)

        if method == "CPF":
            queryset = BasicInfo.objects.filter(numero_documento_CPF = searchid).latest('id')
        elif method == "CNPJ":
            queryset = BasicInfo.objects.filter(numero_documento_CNPJ = searchid).latest('id')
        elif method == "id":
            queryset = BasicInfo.objects.filter(id = searchid)
        
        if not queryset:
            context = {
                "ERROR" : 1,
                "ERROR_HEADER" : "Cliente Não Encontrado.",
                "ERROR_MSG" : "A busca não retornou nenhum cliente. Verifique se o cliente está cadastrado, se não, cadastre-o."
            }

            return render(request, template_name, context)
        
        # Getting Alocated Employees Info
        try:
            contractualinfo = ContractualInfo.objects.filter(basicinfo_id = queryset[0].id)
            context = {
            "SEARCH_OBJ" : queryset[0],
            "SEARCH_OBJ_EMPLOYEES" : contractualinfo[0]
            }
        except TypeError:
            contractualinfo = ContractualInfo.objects.filter(basicinfo_id = queryset.id)
            context = {
            "SEARCH_OBJ" : queryset,
            "SEARCH_OBJ_EMPLOYEES" : contractualinfo[0]
            }
            
    return render(request, template_name, context)