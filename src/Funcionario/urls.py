from django.urls import path
#from Funcionario import views as views_funcionario
from Funcionario.forms import (
    BasicInfoForm,
    AddressInfoForm,
    DocumentsInfoForm,
    ForeignerInfoForm,
    HandicappedInfoForm,
    ContactInfoForm,
    BankingInfoForm,
    AnotherJobInfoForm,
    InternInfoForm,
    ContractualInfoForm,
    DocScansForm,
    CadastroFuncionarioWizard
    )
from .utilities import estagiario_form_condition, estrangeiro_form_condition, outro_emprego_form_condition, deficiente_form_condition
from . import views

create_funcionario_forms = [
    ('Basic Info', BasicInfoForm),
    ('Address Info', AddressInfoForm),
    ('Documents Info', DocumentsInfoForm),
    ('Foreigner Info', ForeignerInfoForm),
    ('Handicapped Info', HandicappedInfoForm),
    ('Contact Info', ContactInfoForm),
    ('Banking Info', BankingInfoForm),
    ('Another Job Info', AnotherJobInfoForm),
    ('Intern Info', InternInfoForm),
    ('Contractual Info', ContractualInfoForm),
    ('Doc Scans', DocScansForm),
]


urlpatterns = [

    # Register URL's
    path('cadastro/', CadastroFuncionarioWizard.as_view(
                                                        create_funcionario_forms,
                                                        condition_dict = {
                                                            'Foreigner Info'    :   estrangeiro_form_condition,
                                                            'Handicapped Info'  :   deficiente_form_condition,
                                                            'Another Job Info'  :   outro_emprego_form_condition,
                                                            'Intern Info'       :   estagiario_form_condition,
                                                            }
                                                        ), name = 'funcionario/cadastro'
    ),
    path('visualizar/<int:id>', CadastroFuncionarioWizard.as_view(
                                                        create_funcionario_forms,
                                                        condition_dict = {
                                                            'Foreigner Info'    :   estrangeiro_form_condition,
                                                            'Handicapped Info'  :   deficiente_form_condition,
                                                            'Another Job Info'  :   outro_emprego_form_condition,
                                                            'Intern Info'       :   estagiario_form_condition,
                                                            }
                                                        ), name = 'funcionario/visualizar'
    ),
    path('cadastro/dependentes/<int:id>', views.cadastroDependentes, name = 'funcionario/cadastro/dependentes' ),

    path('', views.appMenu, name = 'funcionario/menu'),    
    ]
