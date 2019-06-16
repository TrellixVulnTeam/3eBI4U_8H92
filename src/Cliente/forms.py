import os
import re
from django import forms
from django.forms import widgets, modelformset_factory
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from chosen import forms as chosenforms

from .models import BasicInfo, AddressInfo, ContractualInfo
from Funcionario.models import BasicInfo as FuncBasicInfo

class BasicInfoForm(forms.ModelForm):
    class Meta():
        model                   =   BasicInfo
        fields = [
            'nome',
            'nome_responsavel',
            'tipo_pessoa',
            'numero_documento_CPF',
            'numero_documento_CNPJ',
            'servico_ativo',
            'observacoes'
        ]

        labels = {
            'nome'                              :'Nome da Empresa',
            'nome_responsavel'                  :'Nome do Responsável',
            'tipo_pessoa'                       :'Tipo de Pessoa',
            'numero_documento_CPF'              :'Número CPF',
            'numero_documento_CNPJ'             :'Número CNPJ',
            'servico_ativo'                     :'Serviço Ativo',
            'observacoes'                       :'Observações'
        }
        widgets = {
            'nome'                              :   widgets.TextInput,              
            'nome_responsavel'                  :   widgets.TextInput,
            'numero_documento_CPF'              :   widgets.TextInput,
            'numero_documento_CNPJ'             :   widgets.TextInput,
            'servico_ativo'                     :   widgets.CheckboxInput
            }

        error_messages = {
            'numero_documento_CPF'              :   {'invalid' : 'Número de CPF inválido'},
            'numero_documento_CNPJ'             :   {'invalid' : 'Número de CNPJ inválido'}
        }

class AddressInfoForm(forms.ModelForm):
    class Meta():
        model = AddressInfo
        fields = [
            'end_fiscal_CEP',
            'end_fiscal',
            'end_fiscal_numero',
            'end_fiscal_bairro',
            'end_fiscal_complemento',
            'end_fiscal_municipio',
            'end_fiscal_estado',
            'end_fiscal_pais',
            'cont_tel_fixo',
            'cont_tel_fixo_adicional',
            'cont_tel_cel',
            'cont_tel_cel_adicional',
            'cont_email',
            'cont_email_adicional'
        ]

        labels = {
            'end_fiscal_CEP'            :   'CEP', 
            'end_fiscal'                :   'Endereço',
            'end_fiscal_numero'         :   'Número',
            'end_fiscal_bairro'         :   'Bairro',
            'end_fiscal_complemento'    :   'Complemento',
            'end_fiscal_municipio'      :   'Município',
            'end_fiscal_estado'         :   'Estado',
            'end_fiscal_pais'           :   'País',
            'end_servico_CEP'           :   'CEP',
            'cont_tel_fixo'             :   'Telefone Fixo',
            'cont_tel_fixo_adicional'   :   'Telefone Fixo',
            'cont_tel_cel'              :   'Telefone Celular',
            'cont_tel_cel_adicional'    :   'Telefone Celular',
            'cont_email'                :   'E-mail',
            'cont_email_adicional'      :   'E-mail'            
        }

        widgets = {
            'end_fiscal_numero'         :   widgets.TextInput,
            'end_servico_numero'        :   widgets.TextInput,
        }

class ChosenModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChosenModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if self.fields[field].__class__.__name__ in ['ChoiceField', 'TypedChoiceField', 'MultipleChoiceField']:
                choices = self.fields[field].choices
                self.fields[field] = chosenforms.ChosenChoiceField(choices=choices)
            elif self.fields[field].__class__.__name__ in ['ModelChoiceField', 'ModelMultipleChoiceField']:
                queryset = self.fields[field].queryset
                self.fields[field] = chosenforms.ChosenModelMultipleChoiceField(queryset=queryset)

    def label_from_instance(self, obj):
            return obj.primeiro_nome

class ContractualInfoForm(ChosenModelForm):
    class Meta:
        model = ContractualInfo

        fields = [
            'funcionario_atrib'
        ]

        labels = {
            'funcionario_atrib' :   'Funcionários Atribuidos'
        }

TEMPLATES = {
        'Basic Info'        :   'wizard_template_basic_info_cliente.html',
        'Address Info'      :   'wizard_template_address_info_cliente.html',
        'Contractual Info'  :   'wizard_template_contractual_info_cliente.html',
        }

# Form Wizard View Class ----------------------

class CadastroClienteWizard(SessionWizardView):

    file_storage = FileSystemStorage(location = os.path.join(settings.MEDIA_ROOT, 'formwizard_temp_file_storage'))

    def get_template_names(self):
        t = [TEMPLATES[self.steps.current]]
        return t

    def done(self, form_list, form_dict, **kwargs):
        
        # UPDATING OBJECT
        if 'id' in self.kwargs:
            eid = self.kwargs['id']

            for k, v in form_dict.items():
                if k == 'Basic Info' and v.changed_data:
                    cdata = v.cleaned_data
                    basicinfo = BasicInfo.objects.get(id = eid)

                    for attr, value in basicinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('basicinfo.' + attr + ' = "' +  str(cdata[attr]) + '"')

                    basicinfo.data_ultima_modificacao = timezone.now()
                    basicinfo.save()

                elif k == 'Address Info' and v.changed_data:
                    cdata = v.cleaned_data
                    addressinfo = AddressInfo.objects.get(basicinfo = eid)
                    
                    for attr, value in addressinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('addressinfo.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    addressinfo.save()

                elif k == 'Contractual Info' and v.changed_data:
                    cdata = v.cleaned_data
                    contractualinfo = ContractualInfo.objects.get(basicinfo = eid)

                    funcionarios_atribuidos = [x.id for x in list(cdata.get('funcionario_atrib'))]
                    
                    contractualinfo.funcionario_atrib.set(funcionarios_atribuidos)
                    contractualinfo.save()

                    basicinfo = contractualinfo.basicinfo

                    basicinfo.quantidade_funcionarios_alocados = len(funcionarios_atribuidos)
                    basicinfo.save()

        # CREATING OBJECT
        else:
            eid =  False 

            for k, v in form_dict.items():
                if k == 'Basic Info':
                    cdata = v.cleaned_data
                    cdata['data_cadastro'] = timezone.now()
                    cdata['data_ultima_modificacao'] = timezone.now()
                    if cdata['servico_ativo'] == True:
                        cdata['data_inicio_servico'] = timezone.now()
                    basicinfo = BasicInfo.objects.create(**cdata)
                elif k == 'Address Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    AddressInfo.objects.create(**cdata)
                elif k == 'Contractual Info':
                    cdata = v.cleaned_data
                    
                    contractualinfo = ContractualInfo()
                    contractualinfo.basicinfo = basicinfo
                    contractualinfo.save()

                    funcionarios_atribuidos = [x.id for x in list(cdata.get('funcionario_atrib'))]
                    
                    contractualinfo.funcionario_atrib.add(*funcionarios_atribuidos)
                    contractualinfo.save()
                    
                    basicinfo.quantidade_funcionarios_alocados = len(funcionarios_atribuidos)
                    basicinfo.save()
                
        return redirect('/cliente/visualizar/' + (str(eid) if eid else str(basicinfo.id)))

    def get_form_initial(self, step):
        if 'id' in self.kwargs:
            eid = self.kwargs['id']
            if step == 'Basic Info':
                obj = BasicInfo.objects.get(id=eid)
            elif step == "Address Info":
                obj = AddressInfo.objects.get(basicinfo=eid)
            elif step == "Contractual Info":
                obj = ContractualInfo.objects.get(basicinfo=eid)

            modeldict = model_to_dict(obj)
            return modeldict
        else:
            return self.initial_dict.get(step, {})
