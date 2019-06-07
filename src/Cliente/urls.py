from django.urls import path
#from Funcionario import views as views_funcionario
from Cliente.forms import (
    BasicInfoForm,
    AddressInfoForm,
    ContractualInfoForm,
    CadastroClienteWizard
    )
from Cliente import views
    
create_cliente_forms = [
    ('Basic Info', BasicInfoForm),
    ('Address Info', AddressInfoForm)
]


urlpatterns = [

    path('cadastro/', CadastroClienteWizard.as_view(create_cliente_forms), name = 'cliente/cadastro'),
    path('visualizar/<int:id>', CadastroClienteWizard.as_view(create_cliente_forms), name = 'cliente/visualizar'),
    path('', views.appMenu, name = 'cliente/menu'),
    path('api/get_by_name/', views.autocompleteByname, name = 'cliente/autocompleteByName')
    ]
