import os
import re
from django import forms
from django.forms import widgets, modelformset_factory
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpRequest
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib.sessions.backends.db import SessionStore

from ControleAdministrativo.models import FuncionarioCargo, FuncionarioNivel

from .models import (
    BasicInfo,
    AddressInfo,
    DocumentsInfo,
    ContactInfo,
    ForeignerInfo,
    HandicappedInfo,
    BankingInfo,
    AnotherJobInfo,
    InternInfo,
    ContractualInfo,
    DocumentAttachments,
    Dependente
)

# SubClassing ModelChoiceFields for Custom Representation of label_from_instance
class ReadableModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        try:
            return obj.cargo
        except:
            return obj.nivel

# Forms

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
            'estagiario',
            'SEG'      
       
        ]
        labels = {
            'primeiro_nome'                                     :'Nome',
            'ultimo_nome'                                       :'Sobrenome',
            'data_nascimento'                                   :'Data de Nascimento',
            'genero'                                            :'Gênero',
            'nacionalidade'                                     :'Nacionalidade',
            'estado_nascimento'                                 :'Estado de Nascimento',
            'municipio_nascimento'                              :'Município de Nascimento',
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
            'deficiente'                                        :'Possui Alguma Deficiência ?',
            'SEG'                                               :'Funcionário SEG ou Eireli ?'
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
            'deficiente'            :   widgets.CheckboxInput,
            'SEG'                   :   widgets.CheckboxInput
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
            'end_residencia_propria': 'Residência Própria', 
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

class ForeignerInfoForm(forms.ModelForm):
    class Meta():
        model = ForeignerInfo
        fields = [
            'estr_data_chegada',
            'estr_naturalizado',
            'estr_data_naturalizacao',
            'estr_casado_brasileiro',
            'estr_filhos_brasileiros'
        ]
        labels = {
            'estr_data_chegada' : 'Data de Chegada',
            'estr_naturalizado' : 'Naturalizado',
            'estr_data_naturalizacao' : 'Data de Naturalização',
            'estr_casado_brasileiro' : 'Casado(a) com Brasileiro(a)',
            'estr_filhos_brasileiros' : 'Filho(a) com Brasileiros' ,
        }
        widgets = {
            'estr_naturalizado'         : widgets.CheckboxInput,
            'estr_casado_brasileiro'    : widgets.CheckboxInput,
            'estr_filhos_brasileiros'   : widgets.CheckboxInput
        }

class HandicappedInfoForm(forms.ModelForm):
    class Meta():
        model = HandicappedInfo
        fields = [
            'deficiencia_tipo',
            'deficiencia_obs'
        ]
        labels = {
            'deficiencia_tipo' : 'Tipo de Deficiência',
            'deficiencia_obs': 'Observações'
        }

        widgets = {
            'deficiencia_obs'   :   widgets.Textarea
        }

class ContactInfoForm(forms.ModelForm):
    class Meta():
        model = ContactInfo
        fields = [
            'cont_tel_fixo',
            'cont_tel_cel',
            'cont_email_secundario',
            'cont_email_principal',
        ]

        labels = {
            'cont_tel_fixo'             : 'Fixo',
            'cont_tel_cel'              : 'Móvel',
            'cont_email_secundario'     : 'E-Mail Secundário',
            'cont_email_principal'      : 'E-Mail',
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
            'banco_agencia' : 'Agência',
            'banco_tipo_conta' : 'Tipo da Conta',
            'banco_numero_conta_root' : 'Conta'
        }
        widgets = {
        }

class AnotherJobInfoForm(forms.ModelForm):
    class Meta():
        model = AnotherJobInfo
        fields = [
            'vinc_outra_emp_func',
            'vinc_outra_emp_soc',
            'vinc_outra_emp_nome',
            'vinc_outra_emp_CNPJ',
            'vinc_outra_emp_salario',
            'vinc_outra_emp_nome_soc',
            'vinc_outra_emp_CNPJ_soc',
            'vinc_outra_emp_salario_soc',
            'vinc_comentarios'
        ]

        labels = {
            'vinc_outra_emp_func' : 'Funcionario em Outra Empresa (CLT)',
            'vinc_outra_emp_soc' : 'Faz ou Fez Parte de Sociedade em Empresa',
            'vinc_outra_emp_nome' : 'Nome da Empresa',
            'vinc_outra_emp_CNPJ' : 'CNPJ',
            'vinc_outra_emp_salario' : 'Remuneração',
            'vinc_outra_emp_nome_soc' : 'Nome da Empresa',
            'vinc_outra_emp_CNPJ_soc' : 'CNPJ',
            'vinc_outra_emp_salario_soc' : 'Remuneração',
            'vinc_comentarios' : 'Observações'
        }

        widgets = {
            'vinc_outra_emp_func'   :   widgets.CheckboxInput,
            'vinc_outra_emp_soc'    :   widgets.CheckboxInput,
            'vinc_outra_emp_CNPJ'   :   widgets.TextInput,
            'vinc_outra_emp_salario':   widgets.TextInput,
            'vinc_comentarios'      :   widgets.Textarea
        }

class InternInfoForm(forms.ModelForm):
    class Meta():
        model = InternInfo
        fields = [
            'estag_data_inicio',
            'estag_data_fim',
            'estag_obrigatorio',
            'estag_escolaridade',
            'estag_area_atuacao',
            'estag_valor_bolsa',
            'estag_instituto_nome',
            'estag_instituto_CNPJ',
            'estag_instituto_end',
            'estag_instituto_UF',
            'estag_instituto_CEP',
            'estag_instituto_tel',
            'estag_instituto_end_numero',
            'estag_instituto_end_municipio'
        ]
        labels = {
            'estag_data_inicio' : 'Data de Início',
            'estag_data_fim' : 'Data de Fim',
            'estag_obrigatorio' : 'Estágio Obrigatório',
            'estag_escolaridade' : 'Nível de Escolaridade',
            'estag_area_atuacao' : 'Área de Atuação',
            'estag_valor_bolsa' : 'Remuneração (R$)',
            'estag_instituto_nome' : 'Nome',
            'estag_instituto_CNPJ' : 'CNPJ',
            'estag_instituto_end' : 'Endereço',
            'estag_instituto_UF' : 'Estado',
            'estag_instituto_CEP' : 'CEP',
            'estag_instituto_tel' : 'Telefone',
            'estag_instituto_end_numero'    :   'Número',
            'estag_instituto_end_municipio' :   'Município'         
        }
        widgets = {
            'estag_obrigatorio'     :   widgets.CheckboxInput,
            'estag_valor_bolsa'     :   widgets.TextInput,
            'estag_instituto_end_numero'    :   widgets.TextInput
        }

class ContractualInfoForm(forms.ModelForm):

    #def __init__(self, *args, **kwargs):
    #    super(ContractualInfoForm, self).__init__(*args, **kwargs)
    #    self.fields['contrat_cargo_inicial'] = ReadableModelChoiceField(queryset = FuncionarioCargo.objects.all(), label = 'Cargo Inicial', required = False)

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
            'contrat_salario_base',
            'contrat_funcao_cargo',
            'contrat_funcao_nivel',
            'contrat_funcao_gestor',
            'contrat_funcao_CBO',
            'contrat_funcao_descricao',
            'contrat_funcao_nivel_inicial',
            'contrat_data_ultima_alteracao_cargo'
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
            'contrat_salario_atual' : 'Remuneração Atual (R$)',
            'contrat_salario_base' : 'Remuneração Inicial (R$)',
            'contrat_funcao_cargo'  :   'Cargo Atual',
            'contrat_funcao_nivel'  :   'Nível Atual',
            'contrat_funcao_gestor' :   'Cargo de Gestão',
            'contrat_funcao_CBO'    :   'CBO',
            'contrat_funcao_descricao'  :   'Descrição do Cargo',
            'contrat_funcao_nivel_inicial' : 'Nível Inicial',
            'contrat_data_ultima_alteracao_cargo' : 'Data da Última Promoção'
          
        }
        widgets = {
            'contrat_salario_atual' : widgets.TextInput,
            'contrat_salario_base' : widgets.TextInput,
            'contrat_vale_alim' : widgets.CheckboxInput,
            'contrat_vale_ref' : widgets.CheckboxInput,
            'contrat_cesta' : widgets.CheckboxInput,
            'contrat_vale_comb' : widgets.CheckboxInput,
            'contrat_vale_transp' : widgets.CheckboxInput,
            'contrat_funcao_gestor' : widgets.CheckboxInput,
            'contrat_funcao_descricao' : widgets.Textarea

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
            'docscan_CPF' : 'CPF ou CNH',
            'docscan_TE' : 'Título de Eleitor',
            'docscan_CTPS' : 'Carteira de Trabalho - CTPS',
            'docscan_reservista' : 'Reservista',
            'docscan_certidao_nascimento' : 'Certidão de Nascimento',
            'docscan_certidao_casamento' : 'Certidão de Casamento',
            'docscan_comprovante_resid' : 'Comprovante de Residência',
            'docscan_comprovante_escolar' : 'Comprovante de Matricula Escolar',
            'docscan_CV' : 'Curriculum Vitae'
        }

Dependentefmset = modelformset_factory(
    Dependente,
    fields = [
        'grau_parentesco',
        'nome',         
        'data_nascimento',
        'CPF',
        'docscan_certidao_nascimento',
        'docscan_CPF',
        'docscan_vacinacao',
        'docscan_RG'
    ],
    labels = {
        'grau_parentesco' : 'Grau de Parentesco',
        'nome' : 'Nome Completo',         
        'data_nascimento' : 'Data de Nascimento',
        'CPF' : 'Número de CPF',
        'docscan_certidao_nascimento' : 'Certidão de Nascimento',
        'docscan_CPF' : 'CPF',
        'docscan_vacinacao' : 'Carteira de Vacinação',
        'docscan_RG' : 'RG'
    },
    extra = 1
    )


TEMPLATES = {
        'Basic Info'        :   'wizard_template_basic_info.html',
        'Address Info'      :   'wizard_template_address_info.html',
        'Documents Info'    :   'wizard_template_documents_info.html', 
        'Foreigner Info'    :   'wizard_template_foreigner_info.html',
        'Handicapped Info'  :   'wizard_template_handicapped_info.html',
        'Contact Info'      :   'wizard_template_contact_info.html',
        'Banking Info'      :   'wizard_template_banking_info.html',
        'Another Job Info'  :   'wizard_template_anotherjob_info.html',
        'Intern Info'       :   'wizard_template_intern_info.html',
        'Position Info'     :   'wizard_template_position_info.html',
        'Contractual Info'  :   'wizard_template_contractual_info.html',
        'Doc Scans'         :   'wizard_template_doc_scans.html'
        }

class CadastroFuncionarioWizard(SessionWizardView):

    file_storage = FileSystemStorage(location = os.path.join(settings.MEDIA_ROOT, 'formwizard_temp_file_storage'))


    def get_template_names(self):
        t = [TEMPLATES[self.steps.current]]
        return t

    def done(self, form_list, form_dict, **kwargs):
        
        # if ID IN URL PARAMETERS: UPDATE RECORDS
        if 'id' in self.kwargs:
            
            eid = self.kwargs['id']

            for k, v in form_dict.items():
                
                if k == 'Basic Info':
                    cdata = v.cleaned_data
                    basicinfo = BasicInfo.objects.get(id = eid)

                    if 'ativo' in v.changed_data:
                        if cdata['ativo'] == True:
                            basicinfo.data_ultima_ativacao = timezone.localtime(timezone.now())
                        else:
                            basicinfo.data_ultimo_desligamento = timezone.localtime(timezone.now())

                    for attr, value in basicinfo.__dict__.items():
                        if attr in cdata.keys():
                            if not cdata[attr] == "None" and not cdata[attr] == None:
                                exec('basicinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')

                    basicinfo.data_ultima_modificacao = timezone.localtime(timezone.now())
                    basicinfo.data_ultima_ativacao = timezone.localtime(timezone.now())
                    basicinfo.save()

                elif k == 'Address Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try: 
                        addressinfo = AddressInfo.objects.get(basicinfo = eid)
                        
                        for attr, value in addressinfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('addressinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        addressinfo.save()
                    except AddressInfo.DoesNotExist:
                        AddressInfo.objects.create(**cdata)

                elif k == 'Documents Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:
                        documentsinfo = DocumentsInfo.objects.get(basicinfo = eid)

                        for attr, value in documentsinfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('documentsinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        documentsinfo.save()
                    except DocumentsInfo.DoesNotExist:
                        DocumentsInfo.objects.create(**cdata)


                elif k == 'Foreigner Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:
                        foreignerinfo = ForeignerInfo.objects.get(basicinfo = eid)
                        
                        for attr, value in foreignerinfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('foreignerinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        foreignerinfo.save()

                    except ForeignerInfo.DoesNotExist:
                        ForeignerInfo.objects.create(**cdata)


                elif k == 'Handicapped Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:
                        handicappedinfo = HandicappedInfo.objects.get(basicinfo = eid)

                        for attr, value in handicappedinfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('handicappedinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        handicappedinfo.save()
                    except HandicappedInfo.DoesNotExist:
                        HandicappedInfo.objects.create(**cdata)


                elif k == 'Contact Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:
                        contactinfo = ContactInfo.objects.get(basicinfo = eid)

                        for attr, value in contactinfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('contactinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        contactinfo.save()
                    except ContactInfo.DoesNotExist:
                        ContactInfo.objects.create(**cdata)


                elif k == 'Banking Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:    
                        bankinginfo = BankingInfo.objects.get(basicinfo = eid)

                        for attr, value in bankinginfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('bankinginfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        bankinginfo.save()
                    except BankingInfo.DoesNotExist:
                        BankingInfo.objects.create(**cdata)


                elif k == 'Another Job Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:
                        anotherjobinfo = AnotherJobInfo.objects.get(basicinfo = eid)

                        for attr, value in anotherjobinfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('anotherjobinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        anotherjobinfo.save()
                    except AnotherJobInfo.DoesNotExist:
                        AnotherJobInfo.objects.create(**cdata)


                elif k == 'Intern Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:
                        interninfo = InternInfo.objects.get(basicinfo = eid)

                        for attr, value in interninfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('interninfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        interninfo.save()
                    except InternInfo.DoesNotExist:
                        InternInfo.objects.create(**cdata)

                elif k == 'Contractual Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    try:
                        contractualinfo = ContractualInfo.objects.get(basicinfo = eid)

                        for attr, value in contractualinfo.__dict__.items():
                            if attr in cdata.keys():
                                if not cdata[attr] == "None" and not cdata[attr] == None:
                                    exec('contractualinfo.' + attr + ' = """' +  str(cdata[attr]) + '"""')
                        contractualinfo.save()
                    except ContractualInfo.DoesNotExist:
                        ContractualInfo.objects.create(**cdata)


                elif k == 'Doc Scans':
                    #cdata = v.cleaned_data
                    #cdata['basicinfo'] = basicinfo
                    #docscans = DocumentAttachments.objects.get(basicinfo = eid)

                    #for attr, value in docscans.__dict__.items():
                    #    if attr in cdata.keys():
                    #        if not cdata[attr] == "None" and not cdata[attr] == None:
                    #            exec('docscans.' + attr + ' = "' +  str(cdata[attr]) + '"')
                    #docscans.save()
                    savingform = v.save(commit = False)
                    savingform.basicinfo = basicinfo
                    not_empty_data = [ k for k,val in v.cleaned_data.items() if val ]
                    savingform.save(update_fields=not_empty_data)

        # ELSE CREATE NEW RECORDS
        else:
            for k, v in form_dict.items():
                if k == 'Basic Info':
                    cdata = v.cleaned_data
                    cdata['data_ultima_ativacao'] = timezone.localtime(timezone.now())
                    cdata['data_ultima_modificacao'] = timezone.localtime(timezone.now())
                    cdata['status'] = "Funcionário em Atividade"
                    basicinfo = BasicInfo.objects.create(**cdata)
                elif k == 'Address Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    AddressInfo.objects.create(**cdata)
                elif k == 'Documents Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    DocumentsInfo.objects.create(**cdata)
                elif k == 'Foreigner Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    ForeignerInfo.objects.create(**cdata)
                elif k == 'Handicapped Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    HandicappedInfo.objects.create(**cdata)
                elif k == 'Contact Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    ContactInfo.objects.create(**cdata)
                elif k == 'Banking Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    BankingInfo.objects.create(**cdata)
                elif k == 'Another Job Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    AnotherJobInfo.objects.create(**cdata)
                elif k == 'Intern Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    InternInfo.objects.create(**cdata)
                elif k == 'Contractual Info':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    ContractualInfo.objects.create(**cdata)
                elif k == 'Doc Scans':
                    cdata = v.cleaned_data
                    cdata['basicinfo'] = basicinfo
                    DocumentAttachments.objects.create(**cdata)
       
        
        redirectID = self.kwargs.get('id') if self.kwargs.get('id') else basicinfo.id

        return redirect('/funcionario/cadastro/dependentes/{}'.format(redirectID))

    def get_form_initial(self, step):
        if 'id' in self.kwargs:
            eid = self.kwargs['id']
            if step == 'Basic Info':
                try:
                    obj = BasicInfo.objects.get(id=eid)
                except:
                    return self.initial_dict.get(step, {})

            elif step == "Address Info":
                try:
                    obj = AddressInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})

            elif step == "Documents Info":
                try:
                    obj = DocumentsInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})

            elif step == "Contact Info":
                try:
                    obj = ContactInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Foreigner Info":
                try:
                    obj = ForeignerInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Handicapped Info":
                try:
                    obj = HandicappedInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Banking Info":
                try:
                    obj = BankingInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Another Job Info":
                try:
                    obj = AnotherJobInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Intern Info":
                try:
                    obj = InternInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Position Info":
                try:
                    obj = PositionInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Contractual Info":
                try:
                    obj = ContractualInfo.objects.get(basicinfo=eid)
                except:
                    return self.initial_dict.get(step, {})
            
            elif step == "Doc Scans":
                #obj = DocumentAttachments.objects.get(basicinfo=eid)
                return self.initial_dict.get(step, {})

            modeldict = model_to_dict(obj)

            return modeldict
        else:
            return self.initial_dict.get(step, {})

    def get_context_data(self, form, **kwargs):
        context = super(CadastroFuncionarioWizard, self).get_context_data(form=form, **kwargs)
        
        if 'id' in self.kwargs:
            eid = self.kwargs['id']
        
            if self.steps.current == 'Doc Scans':
                try:
                    scans = DocumentAttachments.objects.get(basicinfo = eid)
                    context.update({'currentscans': scans})
                finally:
                    return context
        return context