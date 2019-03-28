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
    PositionInfoForm,
    ContractualInfoForm,
    DocScansForm,
    DependenteForm,
    CadastroFuncionarioWizard
    )
from .utilities import estagiario_form_condition, estrangeiro_form_condition, outro_emprego_form_condition, deficiente_form_condition


create_funcionario = 'cadastro/'
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
    ('Position Info', PositionInfoForm),
    ('Contractual Info', ContractualInfoForm),
    ('Doc Scans', DocScansForm)
]


urlpatterns = [

    # Register URL's
    #path(create_funcionario + '/docscans/', views_funcionario.addFuncionarioDocScans),
    #path(create_funcionario + '/informacoes-iniciais/', views_funcionario.addFuncionarioBasicInfo),
    #path(create_funcionario + '/endereco/', views_funcionario.addFuncionarioAddressInfo),
    #path(create_funcionario + '/documentos/', views_funcionario.addFuncionarioDocumentsInfo),
    #path(create_funcionario + '/outras_informacoes/', views_funcionario.addFuncionarioOtherInfo),
    #path(create_funcionario + '/dados_bancarios/', views_funcionario.addFuncionarioBankingInfo),
    #path(create_funcionario + '/empregos_paralelos/', views_funcionario.addFuncionarioOtherEmploymentInfo),
    #path(create_funcionario + '/estagio/', views_funcionario.addFuncionarioInternInfo),
    #path(create_funcionario + '/cargo/', views_funcionario.addFuncionarioPositionInfo),
    #path(create_funcionario + '/dados_contrato/', views_funcionario.addFuncionarioContractInfo),
    #path(create_funcionario + '/dependentes/', views_funcionario.addDependente),
    path(create_funcionario, CadastroFuncionarioWizard.as_view(
                                                        create_funcionario_forms,
                                                        condition_dict = {
                                                            'Foreigner Info'    :   estrangeiro_form_condition,
                                                            'Handicapped Info'  :   deficiente_form_condition,
                                                            'Another Job Info'  :   outro_emprego_form_condition,
                                                            'Intern Info'       :   estagiario_form_condition,
                                                            }
                                                        )
    ),
    
    
    ]
