from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Dependente, BasicInfo, DocumentAttachments
from .forms import DependenteForm
from .tables import FuncionarioBasicInfoTable
from django.contrib.auth.decorators import login_required

@login_required
def appMenu(request, *args, **kwargs):
    
    table = FuncionarioBasicInfoTable(BasicInfo.objects.all())

    if request.GET:
        
        
        query = request.GET.get('CPF') if request.GET.get('CPF') else request.GET.get('id')
        met   = 'CPF' if request.GET.get('CPF') else 'id'

        if query:
            try:
                biResults = BasicInfo.objects.get(numero_documento_CPF = query) if met == 'CPF' else BasicInfo.objects.get(id = query)
            
            except BasicInfo.MultipleObjectsReturned:
                
                biResults = BasicInfo.objects.filter(numero_documento_CPF = query).latest('id') if met == 'CPF' else BasicInfo.objects.get(id = query)
                scanResults = DocumentAttachments.objects.get(basicinfo = biResults)
                context = {
                    "object"   :   biResults,
                    "imageObject"   :   scanResults,
                    "ERROR"  :   2,
                    "table"  :  table
                }    
                return render(request, 'app_menu.html', context)
                
            except:
                context = {
                    "ERROR"  :   1,
                    "table"  :  table
                }    
                return render(request, 'app_menu.html', context)

            scanResults = DocumentAttachments.objects.get(basicinfo = biResults)
            context = {
                "object"   :   biResults,
                "imageObject"   :   scanResults,
                "table"  :  table
            }   

        else:
            context = {
                "ERROR"  :   2,
                "table"  :  table
            }

        return render(request, 'app_menu.html', context)
    elif request.POST:
        
        bi = BasicInfo.objects.get(id = request.POST.get('shutDownID'))
        
        if bi.ativo == True:
            bi.ativo = False
            bi.data_ultimo_desligamento = timezone.localtime(timezone.now())
            bi.data_ultima_modificacao = timezone.localtime(timezone.now())
            bi.obs_desligamento = str(timezone.localdate()) + ' - ' + request.POST.get('occurrenceShutDown') + "\n" + bi.obs_desligamento if request.POST.get('occurrenceShutDown') != "" else ""
            bi.ferias = False
            bi.save()
            
            return render(request, 'app_menu.html', {"table"  :  table})
        else:
            context = {
                "ERROR"  :   3,
                "table"  :  table
            }

            return render(request, 'app_menu.html', context)
    else:
        return render(request, 'app_menu.html', {"table"  :  table})

@login_required
def funcionariosListing(request, *args, **kwargs):
    table = FuncionarioBasicInfoTable(BasicInfo.objects.all())

    return render(request, 'employee_table_template.html', {'table' : table})

