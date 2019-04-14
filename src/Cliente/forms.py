import os
import re
from django import forms
from django.forms import widgets
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


from .models import (
    BasicInfo,
    AddressInfo,
    DocumentsInfo,
    ContactInfo,
    BankingInfo,
    ContractualInfo,
    DocumentAttachments,
)

class BasicInfoForm(forms.ModelForm):
    class Meta():
        model                   =   BasicInfo
        fields = [
            'primeiro_nome',       
            'ultimo_nome',         
            'data_nascimento',     
            'genero',              
            'nacionalidade',       
            'estado_nascimento',   
            'municipio_nascimento',
            'numero_documento_CPF',
            'numero_inscricao_NIS',
            'numero_PIS_PASEP',    
            'numero_NIT_INSS',     
            'numero_codigo_NIT',   
            'raca_cor',            
            'nome_completo_mae',   
            'nome_completo_pai',   
            'estado_civil',
            'escolaridade',

            'primeiro_emprego',
            'estrangeiro',
            'deficiente',
            'outro_emprego',   
            'estagiario'      
       
        ]
        labels = {
            'primeiro_nome'                                     :'Nome',
            'ultimo_nome'                                       :'Sobrenome',
            'data_nascimento'                                   :'Data de Nascimento',
            'genero'                                            :'Gênero',
            'nacionalidade'                                     :'Nacionalidade',
            'estado_nascimento'                                 :'Estado de Nascimento',
            'municipio_nascimento'                              :'Municipio de Nascimento',
            'numero_documento_CPF'                              :'Número do CPF',
            'numero_inscricao_NIS'                              :'Número do NIS',
            'numero_PIS_PASEP'                                  :'Número PIS PASEP',
            'numero_NIT_INSS'                                   :'Número NIT INSS',
            'numero_codigo_NIT'                                 :'Código NIT',
            'raca_cor'                                          :'Raça/Cor',
            'nome_completo_mae'                                 :'Nome da Mãe',
            'nome_completo_pai'                                 :'Nome do Pai',
            'estado_civil'                                      :'Estado Civil',
            'escolaridade'                                      :'Escolaridade',
            'primeiro_emprego'                                  :'Primeiro Emprego ?',
            'estrangeiro'                                       :'Estrangeiro ?',
            'outro_emprego'                                     :'Possui Outro Emprego ?',   
            'estagiario'                                        :'É Estagiário ?',
            'deficiente'                                        :'Possui Alguma Deficiência ?'
        }
        widgets = {
            'primeiro_nome'         :   widgets.TextInput,
            'ultimo_nome'           :   widgets.TextInput,
            'data_nascimento'       :   widgets.DateInput,
            'nacionalidade'         :   widgets.TextInput,
            'municipio_nascimento'  :   widgets.TextInput,
            'numero_documento_CPF'  :   widgets.TextInput,
            'numero_inscricao_NIS'  :   widgets.TextInput,
            'numero_PIS_PASEP'      :   widgets.TextInput,
            'numero_NIT_INSS'       :   widgets.TextInput,
            'numero_codigo_NIT'     :   widgets.TextInput,
            'nome_completo_mae'     :   widgets.TextInput,
            'nome_completo_pai'     :   widgets.TextInput,
            
            'primeiro_emprego'      :   widgets.CheckboxInput,
            'estrangeiro'           :   widgets.CheckboxInput,
            'outro_emprego'         :   widgets.CheckboxInput,
            'estagiario'            :   widgets.CheckboxInput,
            'deficiente'            :   widgets.CheckboxInput
        }

        error_messages = {
            'data_nascimento'   :   {'invalid' : 'Data de Nascimento Inválida'},
            'numero_documento_CPF'  :   {'invalid' : 'Número de CPF inválido'}
        }

class AddressInfoForm(forms.ModelForm):
    class Meta():
        model = AddressInfo
        fields = [
            'end_residente_exterior',
            'end_geral',
            'end_numero',
            'end_bairro',
            'end_complemento',
            'end_municipio',
            'end_estado',
            'end_CEP',
            'end_pais',
            'end_residencia_propria',
            'end_comprado_FGTS'   
        ]

        labels = {
            'end_residente_exterior': 'Residente no Exterior', 
            'end_geral': 'Endereço', 
            'end_numero': 'Número', 
            'end_bairro': 'Bairro', 
            'end_complemento': 'Complemento', 
            'end_municipio': 'Município', 
            'end_estado': 'Estado', 
            'end_CEP': 'CEP', 
            'end_pais': 'País', 
            'end_residencia_propria': 'Residêcia Própria', 
            'end_comprado_FGTS': 'Comprado com FGTS'
        }

        widgets = {
            'end_residente_exterior'    :   widgets.CheckboxInput,
            'end_numero'                :   widgets.TextInput,
            'end_CEP'                   :   widgets.TextInput,
            'end_residencia_propria'    :   widgets.CheckboxInput,
            'end_comprado_FGTS'         :   widgets.CheckboxInput,
        }

class DocumentsInfoForm(forms.ModelForm):
    class Meta():
        model = DocumentsInfo

        fields = [
            'docs_CTPS_numero_geral',
            'docs_CTPS_numero_serie',
            'docs_CTPS_UF',
            'docs_CTPS_data_emissao',
            'docs_TE_numero_geral',
            'docs_TE_secao',
            'docs_TE_zona',
            'docs_RG_numero_geral',
            'docs_RG_emissor',
            'docs_RG_UF',
            'docs_RG_data_emissao',
            'docs_RNE_numero_geral',
            'docs_RNE_emissor',
            'docs_RNE_UF',
            'docs_RNE_data_emissao',
            'docs_OC_numero_geral',
            'docs_OC_emissor',
            'docs_OC_UF',
            'docs_OC_data_emissao',
            'docs_CNH_numero_geral',
            'docs_CNH_emissor',
            'docs_CNH_UF',
            'docs_CNH_data_emissao',
            'docs_CNH_categoria',
            'docs_CNH_data_primeira',
            'docs_CNH_data_validade'
        ]

        labels = {
            'docs_CTPS_numero_geral': 'Número CTPS', 
            'docs_CTPS_numero_serie': 'Número de Série CTPS', 
            'docs_CTPS_UF': 'UF CTPS', 
            'docs_CTPS_data_emissao': 'Data Emissão CTPS', 
            'docs_TE_numero_geral': 'Número Título', 
            'docs_TE_secao': 'Seção Eleitoral', 
            'docs_TE_zona': 'Zona Eleitoral', 
            'docs_RG_numero_geral': 'Número RG', 
            'docs_RG_emissor': 'Emissor RG', 
            'docs_RG_UF': 'UF RG', 
            'docs_RG_data_emissao': 'Data Emissão RG', 
            'docs_RNE_numero_geral': 'Número RNE', 
            'docs_RNE_emissor': 'Emissor RNE', 
            'docs_RNE_UF': 'UF RNE', 
            'docs_RNE_data_emissao': 'Data Emissão RNE', 
            'docs_OC_numero_geral': 'Número OC', 
            'docs_OC_emissor': 'Emissor OC', 
            'docs_OC_UF': 'UF OC', 
            'docs_OC_data_emissao': 'Data Emissão OC', 
            'docs_CNH_numero_geral': 'Número CNH', 
            'docs_CNH_emissor': 'Emissor CNH', 
            'docs_CNH_UF': 'UF CNH', 
            'docs_CNH_categoria': 'Categoria CNH',
            'docs_CNH_data_primeira': 'Data Primeira CNH', 
            'docs_CNH_data_emissao': 'Data Emissão CNH',  
            'docs_CNH_data_validade': 'Validade CNH'
        }

        widgets = {
            'docs_CTPS_numero_geral'    :   widgets.TextInput,
            'docs_CTPS_numero_serie'    :   widgets.TextInput,
            'docs_CTPS_data_emissao'    :   widgets.DateInput,
            'docs_TE_numero_geral'      :   widgets.TextInput,
            'docs_RG_numero_geral'      :   widgets.TextInput,

        }


class ContactInfoForm(forms.ModelForm):
    class Meta():
        model = ContactInfo
        fields = [
            'cont_tel_fixo',
            'cont_tel_cel',
            'cont_tel_recado',
            'cont_email',
        ]

        labels = {
            'cont_tel_fixo'     : 'Residêncial',
            'cont_tel_cel'      : 'Celular',
            'cont_tel_recado'   : 'Recados',
            'cont_email'        : 'E-Mail',
        }

class BankingInfoForm(forms.ModelForm):
    class Meta():
        model = BankingInfo
        fields = [
            'banco_numero_codigo',
            'banco_nome',
            'banco_agencia',
            'banco_tipo_conta',
            'banco_numero_conta_root'
        ]
        labels = {
            'banco_numero_codigo' : 'Código do Banco',
            'banco_nome' : 'Nome do Banco',
            'banco_agencia' : 'Número de Agência',
            'banco_tipo_conta' : 'Tipo da Conta',
            'banco_numero_conta_root' : 'Número da Conta'
        }
        widgets = {
            'banco_numero_codigo' : widgets.TextInput,
            'banco_agencia' : widgets.TextInput,
        }

class ContractualInfoForm(forms.ModelForm):
    class Meta():
        model = ContractualInfo

        fields = [
            'contrat_data_admissao',
            'contrat_data_inicio',
            'contrat_cargo_inicial',
            'contrat_vale_alim',
            'contrat_vale_alim_valor',
            'contrat_vale_ref',
            'contrat_vale_ref_valor',
            'contrat_cesta',
            'contrat_cesta_valor',
            'contrat_vale_comb',
            'contrat_vale_comb_valor',
            'contrat_vale_transp',
            'contrat_vale_transp_valor',
            'contrat_salario_atual',
            'contrat_salario_base'            
        ]
        labels = {
            'contrat_data_admissao' : 'Data de Admissão',
            'contrat_data_inicio' : 'Data de Inicio',
            'contrat_cargo_inicial' : 'Cargo Inicial',
            'contrat_vale_alim' : 'Vale Alimentação',
            'contrat_vale_alim_valor' : 'Valor do Vale Alimentação (R$)',
            'contrat_vale_ref' : 'Vale Refeição',
            'contrat_vale_ref_valor' : 'Valor do Vale Refeição (R$)',
            'contrat_cesta' : 'Cesta Básica',
            'contrat_cesta_valor' : 'Valor da Cesta Básica (R$)',
            'contrat_vale_comb' : 'Vale Combustível',
            'contrat_vale_comb_valor' : 'Valor do Vale Combustível (R$)',
            'contrat_vale_transp' : 'Vale Transporte',
            'contrat_vale_transp_valor' : 'Valor do Vale transporte (R$)',
            'contrat_salario_atual' : 'Salário Atual (R$)',
            'contrat_salario_base' : 'Salário Base (R$)'            
        }
        widgets = {
            'contrat_salario_atual' : widgets.TextInput,
            'contrat_salario_base' : widgets.TextInput,
            'contrat_vale_alim' : widgets.CheckboxInput,
            'contrat_vale_ref' : widgets.CheckboxInput,
            'contrat_cesta' : widgets.CheckboxInput,
            'contrat_vale_comb' : widgets.CheckboxInput,
            'contrat_vale_transp' : widgets.CheckboxInput,
        }

class DocScansForm(forms.ModelForm):
    class Meta():
        model = DocumentAttachments

        fields = [
            'docscan_picture',
            'docscan_CPF',
            'docscan_TE',
            'docscan_CTPS',
            'docscan_reservista',
            'docscan_certidao_nascimento',
            'docscan_certidao_casamento',
            'docscan_comprovante_resid',
            'docscan_comprovante_escolar',
            'docscan_CV'
        ]
        labels = {
            'docscan_picture' : 'Foto',
            'docscan_CPF' : 'CPF',
            'docscan_TE' : 'Título de Eleitor',
            'docscan_CTPS' : 'Carteira de Trabalho - CTPS',
            'docscan_reservista' : 'Reservista',
            'docscan_certidao_nascimento' : 'Certidão de Nascimento',
            'docscan_certidao_casamento' : 'Certidão de Casamento',
            'docscan_comprovante_resid' : 'Comprovante de Residência',
            'docscan_comprovante_escolar' : 'Comprovante de Matricula Escolar',
            'docscan_CV' : 'Curriculum Vitae'
        }


TEMPLATES = {
        'Basic Info'        :   'wizard_template_basic_info.html',
        'Address Info'      :   'wizard_template_address_info.html',
        'Documents Info'    :   'wizard_template_documents_info.html', 
        'Contact Info'      :   'wizard_template_contact_info.html',
        'Banking Info'      :   'wizard_template_banking_info.html',
        'Contractual Info'  :   'wizard_template_contractual_info.html',
        'Doc Scans'         :   'wizard_template_doc_scans.html'
        }

class CadastroClienteWizard(SessionWizardView):

    file_storage = FileSystemStorage(location = os.path.join(settings.MEDIA_ROOT, 'formwizard_temp_file_storage'))


    def get_template_names(self):
        t = [TEMPLATES[self.steps.current]]
        return t

    def done(self, form_list, form_dict, **kwargs):
        if 'id' in self.kwargs:
            
            eid = self.kwargs['id']

            for k, v in form_dict.items():
                if k == 'Basic Info':
                    cdata = v.cleaned_data
                    basicinfo = BasicInfo.objects.get(id = eid)
                    print(v.changed_data)

                    if 'ativo' in v.changed_data:
                        if cdata['ativo'] == True:
                            basicinfo.data_ultima_ativacao = timezone.now()
                        else:
                            basicinfo.data_ultimo_desligamento = timezone.now()

                    for attr, value in basicinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('basicinfo.' + attr + ' = "' +  str(cdata[attr]) + '"')

                    basicinfo.data_ultima_modificacao = timezone.now()
                    basicinfo.data_ultima_ativacao = timezone.now()
                    basicinfo.save()

                elif k == 'Address Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    addressinfo = AddressInfo.objects.get(basicinfo = eid)
                    
                    for attr, value in addressinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('addressinfo.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    addressinfo.save()

                elif k == 'Documents Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    documentsinfo = DocumentsInfo.objects.get(basicinfo = eid)

                    for attr, value in documentsinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('documentsinfo.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    documentsinfo.save()

                elif k == 'Contact Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    contactinfo = ContactInfo.objects.get(basicinfo = eid)

                    for attr, value in contactinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('contactinfo.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    contactinfo.save()

                elif k == 'Banking Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    bankinginfo = BankingInfo.objects.get(basicinfo = eid)

                    for attr, value in bankinginfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('bankinginfo.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    bankinginfo.save()

                elif k == 'Contractual Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    contractualinfo = ContractualInfo.objects.get(basicinfo = eid)

                    for attr, value in contractualinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('contractualinfo.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    contractualinfo.save()

                elif k == 'Doc Scans':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    docscans = DocumentAttachments.objects.get(basicinfo = eid)

                    for attr, value in docscans.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('docscans.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    docscans.save()



        else:
            for k, v in form_dict.items():
                if k == 'Basic Info':
                    cdata = v.cleaned_data
                    basicinfo = BasicInfo.objects.create(**cdata)
                elif k == 'Address Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    AddressInfo.objects.create(**cdata)
                elif k == 'Documents Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    DocumentsInfo.objects.create(**cdata)
                elif k == 'Contact Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    ContactInfo.objects.create(**cdata)
                elif k == 'Banking Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    BankingInfo.objects.create(**cdata)
                elif k == 'Contractual Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    ContractualInfo.objects.create(**cdata)
                elif k == 'Doc Scans':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    DocumentAttachments.objects.create(**cdata)    

        return redirect('/funcionario/')

    def get_form_initial(self, step):
        if 'id' in self.kwargs:
            eid = self.kwargs['id']
            if step == 'Basic Info':
                obj = BasicInfo.objects.get(id=eid)
            elif step == "Address Info":
                obj = AddressInfo.objects.get(basicinfo=eid)
            elif step == "Documents Info":
                obj = DocumentsInfo.objects.get(basicinfo=eid)
            elif step == "Contact Info":
                obj = ContactInfo.objects.get(basicinfo=eid)
            elif step == "Banking Info":
                obj = BankingInfo.objects.get(basicinfo=eid)
            elif step == "Contractual Info":
                obj = ContractualInfo.objects.get(basicinfo=eid)
            elif step == "Doc Scans":
                obj = DocumentAttachments.objects.get(basicinfo=eid)
                return self.initial_dict.get(step, {})


            modeldict = model_to_dict(obj)
            return modeldict
        else:
            return self.initial_dict.get(step, {})
