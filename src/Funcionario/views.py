from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseNotFound
from django.utils import timezone
from .models import Dependente, BasicInfo, DocumentAttachments
from .forms import Dependentefmset
from .tables import FuncionarioBasicInfoTable
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from datetime import datetime
from . import utilities

@login_required
def appMenu(request, *args, **kwargs):
    
    # GENERIC DEFINITIONS
    table = FuncionarioBasicInfoTable(BasicInfo.objects.all())
    context = {
        'table' : table
    }

    # HANDLING GET METHOD CALL
    if request.GET:
        
        
        query = request.GET.get('CPF') if request.GET.get('CPF') else request.GET.get('id')
        met   = 'CPF' if request.GET.get('CPF') else 'id'

        if query:
            try:
                biResults = BasicInfo.objects.get(numero_documento_CPF = query) if met == 'CPF' else BasicInfo.objects.get(id = query)
            
            except BasicInfo.MultipleObjectsReturned:
                
                biResults = BasicInfo.objects.filter(numero_documento_CPF = query).latest('id') if met == 'CPF' else BasicInfo.objects.get(id = query)
                try:
                    scanResults = DocumentAttachments.objects.get(basicinfo = biResults)
                
                    context.update({
                        "object"   :   biResults,
                        "imageObject"   :   scanResults,
                        "ERROR"  :   2
                    }) 
                    return render(request, 'app_menu.html', context)
                
                except:
                    context.update({
                        "object"   :   biResults,
                        "ERROR"  :   2
                    }) 
                    return render(request, 'app_menu.html', context)

            except:
                context.update({
                    "ERROR"  :   1
                })
                return render(request, 'app_menu.html', context)
            try:
                scanResults = DocumentAttachments.objects.get(basicinfo = biResults)
                context.update({
                    "object"   :   biResults,
                    "imageObject"   :   scanResults
                })
            except:
                context.update({
                    "object"   :   biResults,
                })

        else:
            context.update({
                "ERROR"  :   2
            })

        return render(request, 'app_menu.html', context)
    
    # HANDLING POST METHOD CALL
    elif request.POST:
        
        # INSTANTIATING EMPLOYEE BASIC INFO OBJECT
        bi = BasicInfo.objects.get(id = request.POST.get('shutDownID'))
        
        # GETTING NEW STATUS FOR STATUS UPDATE
        newstatus = request.POST.get('status-selection')
        bi.status = newstatus

        # SHUTING DOWN EMPLOYEE RELATION
        if newstatus == "shutdown" or newstatus == "occurrenceshutdown":
        
            if bi.ativo == True:
                bi.ativo = False
                bi.status = "Funcionário Desligado"
                bi.data_ultimo_desligamento = timezone.localtime(timezone.now())
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())   
        
                if newstatus == "occurrenceshutdown":
                    bi.obs_desligamento = str(timezone.localdate()) + ' - ' + str(request.POST.get('obsfield')) + '\n' + str(bi.obs_desligamento) if request.POST.get('obsfield') != None or request.POST.get('obsfield') != "" else ""
                bi.save()
        
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)

        # STARTING EMPLOYEE VACATION
        if newstatus == "startvacation":
            
            if bi.ferias == False:
                bi.ferias = True
                bi.status = "Funcionário em Férias"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)

        # FINISHING EMPLOYEE VACATION
        if newstatus == "finishvacation":
            
            if bi.ferias == True:
                bi.ferias = False
                bi.status = "Funcionário em Atividade"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)

        # STARTING EMPLOYEE LEAVE
        if newstatus == "startleave":
            
            if bi.afastamento == False:
                bi.afastamento = True
                bi.status = "Funcionário Afastado"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())
                bi.obs_status += str(timezone.localdate()) +' (' + 'AFASTAMENTO' + ')' + ' - ' + str(request.POST.get('obsfield')) + '\n'
  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)

        # FINISHING EMPLOYEE LEAVE
        if newstatus == "finishleave":
            
            if bi.afastamento == True:
                bi.afastamento = False
                bi.status = "Funcionário em Atividade"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)

        # STARTING EMPLOYEE SUSPENSION
        if newstatus == "startsuspension":
            
            if bi.afastamento == False:
                bi.afastamento = True
                bi.status = "Funcionário Suspenso"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())
                bi.obs_status += str(timezone.localdate()) +' (' + 'SUSPENÇÃO' + ')' + ' - ' + str(request.POST.get('obsfield')) + '\n'
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)

        # FINISHING EMPLOYEE SUSPENSION
        if newstatus == "finishsuspension":
            
            if bi.afastamento == True:
                bi.afastamento = False
                bi.status = "Funcionário em Atividade"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)



        # REACTIVATING EMPLOYEE RELATION
        if newstatus == "reactivate":
        
            if bi.ativo == False:
                bi.status = "Funcionário em Atividade"
                bi.ativo = True
                bi.data_ultima_ativacao = timezone.localtime(timezone.now())
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())   
        
                bi.save()
        
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, 'app_menu.html', context)

            # SUCCESS RENDER
            return render(request, 'app_menu.html', context)

        # GENERAL FAILSAFE RENDER
        return render(request, 'app_menu.html', context)
    
    else:
        return render(request, 'app_menu.html', {"table"  :  table})

@login_required
def cadastroDependentes(request, *args, **kwargs):
    template_name = 'wizard_template_dependents.html'

    if request.method == 'GET':
        formset = Dependentefmset(queryset = Dependente.objects.filter(basicinfo = kwargs.get('id')))
        context = {'formset' : formset}


        return render(request, template_name, context)
    
    if request.method == 'POST':
        formset = Dependentefmset(request.POST)
        
        for form in formset:
                        
            if form.is_valid() and form.cleaned_data:
                
               # CASE NEW DEPENDENT
                savingform = form.save(commit = False)
                savingform.basicinfo = BasicInfo.objects.get(id = kwargs.get('id'))
                savingform.save()

        return redirect('funcionario/menu')

class DetalhesFuncionario(View):
    def get(self, request, *args, **kwargs):
        # Template Name
        template_name = "single_employee_menu.html"

        # Check for id in URL
        if not self.kwargs.get('id'):
            return HttpResponseNotFound("<h1>404 Page Not Found !</h1>")
        
        # Return Object Searched For
        searchid = self.kwargs.get('id')
        basicinfo = BasicInfo.objects.get(id = searchid)

        context = {
            'basicinfo' : basicinfo,
            'age'       : basicinfo.age
        }

        return render(request, template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Template Name
        template_name = "single_employee_menu.html"

        # Check for id in URL
        if not self.kwargs.get('id'):
            return HttpResponseNotFound("<h1>404 Page Not Found !</h1>")
        
        # INSTANTIATING EMPLOYEE BASIC INFO OBJECT
        searchid = self.kwargs.get('id')
        bi = BasicInfo.objects.get(id = searchid)

        context = {
            'basicinfo' : bi,
            'age'       : bi.age
        }

        # GETTING NEW STATUS FOR STATUS UPDATE
        newstatus = request.POST.get('status-selection')
        bi.status = newstatus

        # SHUTING DOWN EMPLOYEE RELATION
        if newstatus == "shutdown" or newstatus == "occurrenceshutdown":
        
            if bi.ativo == True:
                bi.ativo = False
                bi.status = "Funcionário Desligado"
                bi.data_ultimo_desligamento = timezone.localtime(timezone.now())
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())   
        
                if newstatus == "occurrenceshutdown":
                    bi.obs_desligamento = str(timezone.localdate()) + ' - ' + str(request.POST.get('obsfield')) + '\n' + str(bi.obs_desligamento) if request.POST.get('obsfield') != None or request.POST.get('obsfield') != "" else ""
                bi.save()
        
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)

        # STARTING EMPLOYEE VACATION
        if newstatus == "startvacation":
            
            if bi.ferias == False:
                bi.ferias = True
                bi.status = "Funcionário em Férias"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)

        # FINISHING EMPLOYEE VACATION
        if newstatus == "finishvacation":
            
            if bi.ferias == True:
                bi.ferias = False
                bi.status = "Funcionário em Atividade"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)

        # STARTING EMPLOYEE LEAVE
        if newstatus == "startleave":
            
            if bi.afastamento == False:
                bi.afastamento = True
                bi.status = "Funcionário Afastado"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())
                bi.obs_status += str(timezone.localdate()) +' (' + 'AFASTAMENTO' + ')' + ' - ' + str(request.POST.get('obsfield')) + '\n'
  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)

        # FINISHING EMPLOYEE LEAVE
        if newstatus == "finishleave":
            
            if bi.afastamento == True:
                bi.afastamento = False
                bi.status = "Funcionário em Atividade"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)

        # STARTING EMPLOYEE SUSPENSION
        if newstatus == "startsuspension":
            
            if bi.afastamento == False:
                bi.afastamento = True
                bi.status = "Funcionário Suspenso"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())
                bi.obs_status += str(timezone.localdate()) +' (' + 'SUSPENÇÃO' + ')' + ' - ' + str(request.POST.get('obsfield')) + '\n'
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)

        # FINISHING EMPLOYEE SUSPENSION
        if newstatus == "finishsuspension":
            
            if bi.afastamento == True:
                bi.afastamento = False
                bi.status = "Funcionário em Atividade"
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())  
                bi.save() 
            
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)



        # REACTIVATING EMPLOYEE RELATION
        if newstatus == "reactivate":
        
            if bi.ativo == False:
                bi.status = "Funcionário em Atividade"
                bi.ativo = True
                bi.data_ultima_ativacao = timezone.localtime(timezone.now())
                bi.data_ultima_modificacao = timezone.localtime(timezone.now())   
        
                bi.save()
        
            else:
                context.update({
                    "ERROR" : 3
                })

                # ERROR RENDER
                return render(request, template_name, context)

            # SUCCESS RENDER
            return render(request, template_name, context)

        # GENERAL FAILSAFE RENDER
        return render(request, template_name, context)