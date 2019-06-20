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
    path('LS/<int:id>', views.ServiceGroundView.as_view(), name = 'cliente/LS'),
    path('gerar-OS/<int:id>', views.ServiceOrderView.as_view(), name = 'cliente/gerar-OS'),
    path('OS/<int:OSid>', views.VisualizeServiceOrderView.as_view(), name = 'cliente/OS'),
    path('editar/<int:id>', CadastroClienteWizard.as_view(create_cliente_forms), name = 'cliente/editar'),
    path('visualizar/<int:id>', views.DetalhesCliente.as_view(), name = 'cliente/visualizar'),
    path('', views.appMenu, name = 'cliente/menu'),
    # API
    path('api/get_by_name/', views.autocompleteByname, name = 'cliente/autocompleteByName')
    ]
