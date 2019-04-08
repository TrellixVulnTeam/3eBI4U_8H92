from django.shortcuts import render, redirect
from .models import Dependente, BasicInfo, DocumentAttachments
from .forms import DependenteForm

def appMenu(request, *args, **kwargs):
    
    if request.GET:
        query = request.GET.get('CPF')
        if query:
            try:
                biResults = BasicInfo.objects.get(numero_documento_CPF = query)
            except:
                context = {"ERROR"  :   1}    
                return render(request, 'app_menu.html', context)

            scanResults = DocumentAttachments.objects.get(basicinfo = biResults)
            context = {
                "object"   :   biResults,
                "imageObject"   :   scanResults
            }   

        else:
            context = {
                "ERROR"  :   2
            }

        return render(request, 'app_menu.html', context)
    else:
        return render(request, 'app_menu.html', {})
