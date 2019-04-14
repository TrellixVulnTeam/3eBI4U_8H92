from django.urls import path
#from Funcionario import views as views_funcionario
from Cliente.forms import (
    BasicInfoForm,
    AddressInfoForm,
    DocumentsInfoForm,
    ContactInfoForm,
    BankingInfoForm,
    ContractualInfoForm,
    DocScansForm,
    CadastroClienteWizard
    )

create_cliente_forms = [
    ('Basic Info', BasicInfoForm),
    ('Address Info', AddressInfoForm),
    ('Documents Info', DocumentsInfoForm),
    ('Contact Info', ContactInfoForm),
    ('Banking Info', BankingInfoForm),
    ('Contractual Info', ContractualInfoForm),
    ('Doc Scans', DocScansForm)
]


urlpatterns = [

    path('cadastro/', CadastroClienteWizard.as_view(
                                                        create_cliente_forms
                                                        )
    ),
    path('visualizar/<int:id>', CadastroClienteWizard.as_view(
                                                        create_cliente_forms
                                                        
                                                        )
    ),
    
    ]
