from django.urls import path
#from Funcionario import views as views_funcionario
from Cliente.forms import (
    BasicInfoForm,
    AddressInfoForm,
    ContactInfoForm,
    ContractualInfoForm,
    CadastroClienteWizard
    )
from Cliente import views
    
create_cliente_forms = [
    ('Basic Info', BasicInfoForm),
    ('Address Info', AddressInfoForm),
    ('Contact Info', ContactInfoForm),
    ('Contractual Info', ContractualInfoForm),
]


urlpatterns = [

    path('cadastro/', CadastroClienteWizard.as_view(create_cliente_forms), name = 'cliente/cadastro'),
    path('visualizar/<int:id>', CadastroClienteWizard.as_view(create_cliente_forms), name = 'cliente/visualizar'),
    path('', views.appMenu, name = 'cliente/menu')
    ]
