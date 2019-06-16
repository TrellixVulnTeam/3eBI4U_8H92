from json import dumps
from django.shortcuts import render, HttpResponse
from django.http.response import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .utilities import validateCNPJ, validateCPF
from django.core.exceptions import ValidationError
from .models import BasicInfo, ContractualInfo
from .tables import ClienteBasicInfoTable
from django.views import View
from django.contrib.auth import authenticate


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
                "ERROR_HEADER" : "Método desconhecido.",
                "ERROR_MSG" : "O Método de Busca Informado é Desconhecido."
            })

            return render(request, template_name, context)

        try:
            if method == "CPF":
                queryset = BasicInfo.objects.filter(numero_documento_CPF = searchid).latest('id')
            elif method == "CNPJ":
                queryset = BasicInfo.objects.filter(numero_documento_CNPJ = searchid).latest('id')
            elif method == "ID":
                queryset = BasicInfo.objects.get(id = searchid)
            elif method == "NOME":
                queryset = BasicInfo.objects.filter(nome = searchid).latest('id')
        
        except:
            context.update({
                "ERROR" : 1,
                "ERROR_HEADER" : "Cliente Não Encontrado.",
                "ERROR_MSG" : "A Busca Não Retornou Nenhum Cliente."
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

class DetalhesCliente(View):
    def get(self, request, *args, **kwargs):
        # Template Name
        template_name = "single_customer_menu.html"
        context = {}

        # Check for id in URL
        if not self.kwargs.get('id'):
            return HttpResponseNotFound("<h1>404 Page Not Found !</h1>")
        
        # Return Object Searched For
        searchid = self.kwargs.get('id')
        
        try:
            basicinfo = BasicInfo.objects.get(id = searchid)

        except BasicInfo.DoesNotExist:
            context.update({
                'basicinfo' : None,
                'ERROR' : True,
                'ERROR_HEADER' : 'Cliente Inexistente.',
                'ERROR_MSG' : 'O cliente buscado não existe.'
            })

            return render(request, template_name, context)    

        context.update({
            'basicinfo' : basicinfo,
        })

        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        
        template_name = "single_customer_menu.html"
        
        # Return Object Searched For
        searchid = self.kwargs.get('id')
        basicinfo = BasicInfo.objects.get(id = searchid)

        context = {
            'basicinfo' : basicinfo,
        }

        username, password = request.POST['username'], request.POST['password']
                
        user = authenticate(username = username, password = password)
        
        if not user:
            context.update({
                "ERROR" :   True,
                "ERROR_HEADER"  :   "Falha de Confirmação.",
                "ERROR_MSG"     :   "Senha inválida para esta sessão."
            })

            return render(request, template_name, context)
        
        client = BasicInfo.objects.filter(id = request.POST['clientID']).latest('id')

        if request.POST.get('operation') == "startService":
            
            if not client.servico_ativo:
                client.servico_ativo = True
                client.data_ultima_modificacao = timezone.now()
                client.data_inicio_servico = timezone.now()
                client.save()
            else:
                context.update({
                    "ERROR" :   True,
                    "ERROR_HEADER"  :   "Serviço Ativo.",
                    "ERROR_MSG"     :   "Não existem serviços inativos para este cliente."
                })

                return render(request, template_name, context)

        else:
            if client.servico_ativo:
                client.servico_ativo = False
                client.data_ultima_modificacao = timezone.now()
                client.data_fim_servico = timezone.now()
                client.save()
            else:
                context.update({
                    "ERROR" :   True,
                    "ERROR_HEADER"  :   "Serviço Inativo.",
                    "ERROR_MSG"     :   "Não existem serviços ativos para este cliente."
                })

                return render(request, template_name, context)

        return render(request, template_name, context)