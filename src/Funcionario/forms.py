import os
import re
from django import forms
from django.forms import widgets
from django.http import HttpResponse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage


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
    PositionInfo,
    ContractualInfo,
    DocumentAttachments,
    Dependente
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

class ForeignerInfoForm(forms.ModelForm):
    class Meta():
        model = ForeignerInfo
        fields = [
            'estr_data_chegada',
            'estr_naturalizado',
            'estr_data_naturalizacao',
            'estr_casado_brasileiro',
        ]
        labels = {
            'estr_data_chegada' : 'Data de Chegada',
            'estr_naturalizado' : 'Naturalizado',
            'estr_data_naturalizacao' : 'Data de Naturalização',
            'estr_casado_brasileiro' : 'Casado(a) com Brasileiro(a)',
            'estr_filhos_brasileiros' : 'Filho(a) de Brasileiros' ,
        }
        widgets = {
            'estr_naturalizado'         : widgets.CheckboxInput,
            'estr_casado_brasileiro'    : widgets.CheckboxInput
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

class AnotherJobInfoForm(forms.ModelForm):
    class Meta():
        model = AnotherJobInfo
        fields = [
            'vinc_outra_emp_func',
            'vinc_outra_emp_soc',
            'vinc_outra_emp_nome',
            'vinc_outra_emp_CNPJ',
            'vinc_outra_emp_salario',
            'vinc_comentarios'
        ]

        labels = {
            'vinc_outra_emp_func' : 'Funcionario em Outra Empresa',
            'vinc_outra_emp_soc' : 'Sócio em Outra Empresa',
            'vinc_outra_emp_nome' : 'Nome da Empresa',
            'vinc_outra_emp_CNPJ' : 'CNPJ da Empresa',
            'vinc_outra_emp_salario' : 'Salário',
            'vinc_comentarios' : 'Comentários'
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
            'estag_instituto_tel'            
        ]
        labels = {
            'estag_data_inicio' : 'Data de Início',
            'estag_data_fim' : 'Data de Fim',
            'estag_obrigatorio' : 'Estágio Obrigatório',
            'estag_escolaridade' : 'Nível de Escolaridade',
            'estag_area_atuacao' : 'Área de Atuação',
            'estag_valor_bolsa' : 'Valor da Bolsa',
            'estag_instituto_nome' : 'Nome',
            'estag_instituto_CNPJ' : 'CNPJ',
            'estag_instituto_end' : 'Endereço',
            'estag_instituto_UF' : 'Estado',
            'estag_instituto_CEP' : 'CEP',
            'estag_instituto_tel' : 'Telefone'            
        }
        widgets = {
            'estag_obrigatorio'     :   widgets.CheckboxInput,
            'estag_valor_bolsa'     :   widgets.TextInput   
        }

class PositionInfoForm(forms.ModelForm):
    class Meta():
        model = PositionInfo
        fields = [
            'funcao_cargo',
            'funcao_nivel',
            'funcao_gestor',
            'funcao_CBO',
            'funcao_descricao'
        ]
        labels = {
            'funcao_cargo'      : 'Cargo',
            'funcao_nivel'      : 'Nível',
            'funcao_gestor'     : 'Cargo de Gestão',
            'funcao_CBO'        : 'CBO da Função',
            'funcao_descricao'  : 'Descrição da Função'
        }
        widgets = {
            'funcao_gestor' : widgets.CheckboxInput,
            'funcao_descricao' : widgets.Textarea
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
            'contrat_vale_alim_valor' : 'Valor do Vale Alimentação',
            'contrat_vale_ref' : 'Vale Refeição',
            'contrat_vale_ref_valor' : 'Valor do Vale Refeição',
            'contrat_cesta' : 'Cesta Básica',
            'contrat_cesta_valor' : 'Valor da Cesta Básica',
            'contrat_vale_comb' : 'Vale Combustível',
            'contrat_vale_comb_valor' : 'Valor do Vale Combustível',
            'contrat_vale_transp' : 'Vale Transporte',
            'contrat_vale_transp_valor' : 'Valor do Vale transporte',
            'contrat_salario_atual' : 'Salário Atual',
            'contrat_salario_base' : 'Salário Base'            
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

class DependenteForm(forms.ModelForm):
    class Meta():
        model = Dependente

        fields = [
            'grau_parentesco',
            'nome',         
            'data_nascimento',
            'CPF',
            'docscan_certidao_nascimento',
            'docscan_CPF',
            'docscan_vacinacao',
            'docscan_RG'
        ]
        labels = {
            'grau_parentesco' : 'Grau de Parentesco',
            'nome' : 'Nome Completo',         
            'data_nascimento' : 'Data de Nascimento',
            'CPF' : 'Número de CPF',
            'docscan_certidao_nascimento' : 'Certidão de Nascimento',
            'docscan_CPF' : 'CPF',
            'docscan_vacinacao' : 'Carteira de Vacinação',
            'docscan_RG' : 'RG'
        }

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
   
    file_storage = FileSystemStorage(
        location = os.path.join(settings.MEDIA_ROOT, 'formwizard_temp_file_storage')
        )

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):
        
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
            elif k == 'Position Info':
                cdata = v.cleaned_data
                cdata['basicinfo'] = basicinfo
                PositionInfo.objects.create(**cdata)
            elif k == 'Contractual Info':
                cdata = v.cleaned_data
                cdata['basicinfo'] = basicinfo
                ContractualInfo.objects.create(**cdata)
            elif k == 'Doc Scans':
                cdata = v.cleaned_data
                cdata['basicinfo'] = basicinfo
                DocumentAttachments.objects.create(**cdata)

        return HttpResponse('yatta')
    
