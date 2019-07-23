from django.views import View
from django.views.generic.edit import CreateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.db import transaction
from django.shortcuts import render, HttpResponse, redirect, render_to_response
from django.http.response import HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils import timezone
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.template import RequestContext
from django.template.loader import render_to_string
from .models import BasicInfo, ContractualInfo, ServiceGround, ServiceDescription, ServiceOrder, ServiceRecord, OccurrenceCall
from Funcionario.models import BasicInfo as Funcionario
from .tables import ClienteBasicInfoTable
from .utilities import validateCNPJ, validateCPF
from .forms import ServiceGroundFormSet, ServiceFormSet, ServiceOrderForm, ServiceRecordForm, LSListing, OccurrenceCallForm, OccurrenceCallEditionForm
from json import dumps
import re, time

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

class DetalhesCliente(View):

    template_name = "single_customer_menu.html"
    context = {}

    def get(self, request, *args, **kwargs):

        context = RequestContext(self.request)

        # Check for id in URL
        if not self.kwargs.get('id'):
            return HttpResponseNotFound("<h1>404 Page Not Found !</h1>")
        
        # Return Object Searched For
        searchid = self.kwargs.get('id')
        
        try:
            basicinfo = BasicInfo.objects.get(id = searchid)

        except BasicInfo.DoesNotExist:
            self.context.update({
                'basicinfo' : None,
                'ERROR' : True,
                'ERROR_HEADER' : 'Cliente Inexistente.',
                'ERROR_MSG' : 'O cliente buscado não existe.'
            })

            return render(request, self.template_name, self.context)    

        self.context.update({
            'basicinfo' : basicinfo
        })

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
                
        # Return Object Searched For
        searchid = self.kwargs.get('id')
        basicinfo = BasicInfo.objects.get(id = searchid)

        self.context.update({
            'basicinfo' : basicinfo,
        })

        username, password = request.POST['username'], request.POST['password']
                
        user = authenticate(username = username, password = password)
        
        if not user:
            self.context.update({
                "ERROR" :   True,
                "ERROR_HEADER"  :   "Falha de Confirmação.",
                "ERROR_MSG"     :   "Senha inválida para esta sessão."
            })

            return render(request, self.template_name, self.context)
        
        client = BasicInfo.objects.filter(id = request.POST['clientID']).latest('id')

        if request.POST.get('operation') == "startService":
            
            if not client.servico_ativo:
                client.servico_ativo = True
                client.data_ultima_modificacao = timezone.now()
                client.data_inicio_servico = timezone.now()
                client.save()
            else:
                self.context.update({
                    "ERROR" :   True,
                    "ERROR_HEADER"  :   "Serviço Ativo.",
                    "ERROR_MSG"     :   "Não existem serviços inativos para este cliente."
                })

                return render(request, self.template_name, self.context)

        else:
            if client.servico_ativo:
                client.servico_ativo = False
                client.data_ultima_modificacao = timezone.now()
                client.data_fim_servico = timezone.now()
                client.save()
            else:
                self.context.update({
                    "ERROR" :   True,
                    "ERROR_HEADER"  :   "Serviço Inativo.",
                    "ERROR_MSG"     :   "Não existem serviços ativos para este cliente."
                })

                return render(request, self.template_name, self.context)

        return render(request, self.template_name, self.context)

class ServiceGroundView(View):
    
    template_name = "service_ground.html"
    context = {}

    def get(self, request, *args, **kwargs):

        formset = ServiceGroundFormSet(queryset = ServiceGround.objects.filter(cliente = kwargs.get('id')))
        self.context.update({
            'formset' : formset,
            'ID' : kwargs.get('id'),
            'base_return_url' : 'cliente/visualizar'
        })

        return render(request, self.template_name, self.context)
    
    def post(self, request, *args, **kwargs):
        formset = ServiceGroundFormSet(request.POST)

        given_objs = []

        for form in formset:

            if form.is_valid() and form.cleaned_data:
                
                savingform = form.save(commit = False)
                savingform.cliente = BasicInfo.objects.get(id = kwargs.get('id'))
                
                given_objs.append(savingform)

                savingform.save()

        current_objs = ServiceGround.objects.filter(cliente = kwargs.get('id'))

        for obj in current_objs:
            if obj not in given_objs:
                obj.delete()

        return redirect('cliente/visualizar', kwargs.get('id'))

class ServiceOrderView(View):

    template_name = 'generate_service_order.html'
    context = {}

    def get(self, request, *args, **kwargs):

        # Creating Service Order for Fixing OS Number and Client to Give the Form 
        ServiceOrderObj = ServiceOrder()
        ServiceOrderObj.cliente = BasicInfo.objects.filter(id = self.kwargs.get('id')).latest('id')
        ServiceOrderObj.save()
        
        formset = ServiceFormSet(instance = ServiceOrderObj)
        
        form = ServiceOrderForm(instance = ServiceOrderObj)
        form.fields['local_servico'].queryset = ServiceGround.objects.filter(cliente = ServiceOrderObj.cliente)

        self.context.update({
            'service_description'   :   formset,
            'form'                  :   form, 
            'emissão'               :   timezone.now().date(),
            'OS'                    :   ServiceOrderObj
        })
        
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        ServiceOrderObj = ServiceOrder.objects.get(id = request.POST.get('OSid'))

        formset = ServiceFormSet(request.POST or None, instance = ServiceOrderObj)
        form = ServiceOrderForm(request.POST or None, instance = ServiceOrderObj)

        if formset.is_valid() and form.is_valid():
            form.save()
            formset.save() 
        else:
            print('Deletando OS {}'.format(request.POST.get('OSid')))
            ServiceOrderObj.delete()


        return redirect('cliente/OS/lista', kwargs.get('id'))

class VisualizeServiceOrderView(View):
    template_name = 'service_order.html'
    context = {}
    def get(self, request, *args, **kwargs):
        
        OSCode = str(kwargs.get('OSid'))
        pattern = re.compile('(^[0-9]{6})([0-9]+$)')
        OSId = re.match(pattern, OSCode).group(2)
        OS = ServiceOrder.objects.get(id = OSId)

        self.context.update({
            'OS' : OS
        })

        return render(request, self.template_name, self.context)

class DeleteOSView(PermissionRequiredMixin, DeleteView):
    model = ServiceOrder
    permission_required = "ServiceOrder.delete_serviceorder"
    success_message = "Ordem de Serviço Deletada com Sucesso !"
    template_name = 'delete_confirmation_OS.html'
    

    def get_object(self, queryset=None):
        obj = super(DeleteOSView, self).get_object()
        self.cliente = obj.cliente.id
        return obj

    def get_context_data(self, **kwargs):
        context = super(DeleteOSView, self).get_context_data(self, **kwargs)
        context.update({
            'ERROR' : True,
            'ERROR_HEADER'  :   ''
        })

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteOSView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('cliente/OS/lista', kwargs = {'id' : self.cliente})

class ListOSView(PermissionRequiredMixin, ListView):
    
    permission_required = "ServiceOrder.can_view_OSList"
    raise_exception = False
    
    template_name = 'list_OS.html'
    paginate_by = 8

    def get_queryset(self):
        #filter_val = self.request.GET.get('filter', 'give-default-value')
        #order = self.request.GET.get('orderby', 'give-default-value')
        cliente = self.kwargs.get('id')
        context = ServiceOrder.objects.filter(cliente = cliente).order_by('-id')
        return context
    
    def get_context_data(self, **kwargs):
        context = super(ListOSView, self).get_context_data(**kwargs)
        context.update({
            'clientID'  :   self.kwargs.get('id'),
            'cliente'   :   BasicInfo.objects.get(id = self.kwargs.get('id'))
        })
        return context
    
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'Você não possui permissão de acesso !')
        return redirect('cliente/visualizar', id = self.kwargs.get('id'))

class CreateReportView(View):
    
    template_name = "service_record.html"
    context = {'read-only' : False}

    form = ServiceRecordForm()

    def get(self, request, *args, **kwargs):

        if self.kwargs.get('id') == 0:
            
            messages.warning(self.request, 'Favor Selecionar o Local de Serviço !')
            return redirect(self.request.META.get('HTTP_REFERER'))

        LS = ServiceGround.objects.get(id = self.kwargs.pop('id'))
        cliente = LS.cliente

        if LS.service_record.filter(data = timezone.localdate()):
            SR = LS.service_record.get(data = timezone.localdate())
        else:
            SR = None
        
        self.context.update({
            'cliente'   : cliente,
            'LS'        : LS,
            'SR'        : SR,
            'data'      : timezone.localdate,
            'form'      : self.form
        })

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):

        LS = ServiceGround.objects.get(id = self.kwargs.pop('id'))
        cliente = LS.cliente

        if LS.service_record.filter(data = timezone.localdate()):
            SR = LS.service_record.get(data = timezone.localdate())
        else:
            SR = None

        form = ServiceRecordForm(request.POST)
        
        if form.is_valid():
            base_description = str(form.cleaned_data.pop('description'))
            description = '[{} - {}] — {}'.format(str(request.user.get_full_name()), str(timezone.localtime().strftime("%H:%M:%S")), base_description)
            if not SR:
                SR = ServiceRecord.objects.create(LS = LS, description = description)
            else:
                for last_entry in re.finditer(r"\[.*\] — ", SR.description):
                    pass
                
                if last_entry:
                    if not SR.description[last_entry.end():] == base_description:
                        SR.description += "\n\n" + description
                        SR.save()

        self.context.update({
            'cliente'   : cliente,
            'LS'        : LS,
            'SR'        : SR,
            'data'      : timezone.localdate,
            'form'      : self.form
        })

        return render(request, self.template_name, self.context)    

class SelectReportView(View):
    template_name = "report_select.html"
    context = {}
    def get(self, request, *args, **kwargs):
        cliente = self.kwargs.pop('id')
        form = LSListing(cliente = cliente)
        self.context.update({
            'form' : form,
            'cliente' : BasicInfo.objects.get(id = cliente)
        })

        return render(request, self.template_name, self.context)

class ReportView(View):
    template_name = "service_record.html"
    context = {'read-only' : False}
    form = ServiceRecordForm()

    def get(self, request, *args, **kwargs):
        SR = ServiceRecord.objects.get(id = self.kwargs.pop('id'))
        LS = SR.LS

        self.context.update({
            'SR'        : SR,
            'LS'        : LS,
            'data'      : timezone.localdate,
            'form'      : self.form
        })

        return render(request, self.template_name, self.context)

class OccurrenceCallCreationView(PermissionRequiredMixin, View):
    template_name = 'occurrence_call/occurrence_call_create.html'
    permission_required = "Cliente.add_occurrencecall"
    form = OccurrenceCallForm()
    context = {'form' : form}

    def get(self, request, *args, **kwargs):

        if self.kwargs.get('id') == 0:
            messages.warning(self.request, 'Favor Selecionar o Local de Serviço !')
            return redirect(self.request.META.get('HTTP_REFERER'), permanent = True)

        LS = ServiceGround.objects.get(id = self.kwargs.pop('id'))
        self.context.update({'LS' : LS})
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = OccurrenceCallForm(request.POST)

        if form.is_valid():
            LS = ServiceGround.objects.get(id = self.kwargs.pop('id'))
            motive = form.cleaned_data.get('description')
            description = "[{} - {} - CHAMADO ABERTO] — {}".format(str(request.user.get_full_name()), str(timezone.localtime().strftime("%d/%m/%Y %H:%M:%S")), motive)
            status = "Aberto"
            Occurrence = OccurrenceCall.objects.create(LS = LS, status = status, description = description, motive = motive)

        messages.success(request, 'Chamado #{} aberto com sucesso !'.format(Occurrence.OC))

        return redirect('cliente/chamado/selecionar', id=LS.cliente.id, permanent = True)
    
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'Você não possui permissão de acesso !')
        return redirect('cliente/visualizar', id = self.kwargs.get('id'))

class OccurrenceCallSelectionView(View):
    template_name = "occurrence_call/occurrence_call_select.html"
    context = {}

    def get(self, request, *args, **kwargs):
        cliente = self.kwargs.pop('id')
        form = LSListing(cliente = cliente)
        self.context.update({
            'form' : form,
            'cliente' : BasicInfo.objects.get(id = cliente)
        })

        return render(request, self.template_name, self.context)
    
    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'Você não possui permissão de acesso !')
        return redirect('cliente/visualizar', id = self.kwargs.get('id'))

class OccurrenceCallView(PermissionRequiredMixin, View):
    template_name = "occurrence_call/occurrence_call.html"
    context = {}
    permission_required = 'Cliente.occurrence_manage'

    def get(self, request, *args, **kwargs):
        OC = OccurrenceCall.objects.get(id = self.kwargs.pop('id'))

        self.context.update({
            'OC' : OC
        })

        return render(request, self.template_name, self.context)

    def handle_no_permission(self):
        # add custom message
        messages.error(self.request, 'Você não possui permissão de acesso !')
        return redirect('cliente/visualizar', id = self.kwargs.get('id'))

class OccurrenceCallEditionView(View):
    template_name = 'occurrence_call/occurrence_call_edit.html'
    form = OccurrenceCallEditionForm()

    context = {}

    def get(self, request, *args, **kwargs):

        OC = OccurrenceCall.objects.get(id = self.kwargs.pop('id'))
        form = OccurrenceCallEditionForm(initial = {'status' : OC.status})

        self.context.update({
            'form' : form,
            'OC'   : OC
            })

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        OC = OccurrenceCall.objects.get(id = self.kwargs.pop('id'))

        form = OccurrenceCallEditionForm(request.POST)

        if form.is_valid():
            status = str(form.cleaned_data.pop('status'))
            base_description = str(form.cleaned_data.pop('description'))
            description = "[{} - {} - {}] — {}".format(str(request.user.get_full_name()), str(timezone.localtime().strftime("%d/%m/%Y %H:%M:%S")), "CHAMADO " + status.upper(), base_description)
            
            for last_entry in re.finditer(r"\[.*\] — ", OC.description):
                pass
                
            if last_entry:
                if not OC.description[last_entry.end():] == base_description:
                    OC.description += "\n\n" + description
                    OC.status = status
                    OC.save()

        form = OccurrenceCallEditionForm(initial = {'status' : OC.status })
        messages.success(request, 'Chamado #{} editado com sucesso.'.format(OC.OC))


        self.context.update({
            'form' : form,
            'OC'   : OC
            })


        return render(request, self.template_name, self.context)

# API Views ----------------------------------------------------------------------------------------------------------------
# AJAX Calls Processing
def autocompleteByname(request, *args, **kwargs):

    if request.is_ajax():
        term = request.GET.get('term', '')
        names = BasicInfo.objects.filter(nome__contains = term)[:20]

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

    return HttpResponse(data, mimetype)

def filterEmployeeDropDown(request, *args, **kwargs):
    category    = request.GET.get('categoria', None)
    if not category == '---------' and category:
        employees   =   Funcionario.objects.filter(categoria = category)
    else:
        employees   =   Funcionario.objects.all()
    return render(request, 'OS_employee_dropdown.html', {'employees' : employees})

def ListaReports(request, *args, **kwargs):
    LS = request.GET.get('LS')
    reports = ServiceRecord.objects.filter(LS = LS)
    base_url_visualizar = "cliente/report/visualizar"
    data = {
        'list'    :   reports,
        'base_url_visualizar' : base_url_visualizar
        }

    return HttpResponse(render_to_string('list_items.html', data))

@permission_required('Cliente.occurrence_listing_viewer', raise_exception=True)
def ListaOccurrences(request, *args, **kwargs):
    LS = request.GET.get('LS')
    occurrences = OccurrenceCall.objects.filter(LS = LS).order_by('-id')
    base_url_visualizar = "cliente/chamado/visualizar"
    data = {
        'list'    :   occurrences,
        'base_url_visualizar' : base_url_visualizar
        }

    return HttpResponse(render_to_string('list_items.html', data))

# Utility Views
def deleteBlankOS(request, *args, **kwargs):
    
    clientID = kwargs.get('id')
    fullOS = ServiceOrder.objects.filter(cliente = clientID)
    delOS = []

    for OS in fullOS:
        if OS.is_empty:
            delOS.append(OS.OS)
            OS.delete()
    
    success_message = " {} Ordens de Serviço Deletadas com Sucesso !".format(str(len(delOS))) if len(delOS) > 0 else "Nenhuma Ordem de Serviço Inválida foi Encontrada."
    messages.success(request, success_message)


    return redirect('cliente/OS/lista', id = clientID)