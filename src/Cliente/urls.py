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
    path('visualizar/<int:id>', views.DetalhesCliente.as_view(), name = 'cliente/visualizar'),
    path('LS/<int:id>', views.ServiceGroundView.as_view(), name = 'cliente/LS'),
    path('OS/<int:OSid>', views.VisualizeServiceOrderView.as_view(), name = 'cliente/OS'),
    path('OS/gerar/<int:id>', views.ServiceOrderView.as_view(), name = 'cliente/OS/gerar'),
    path('OS/excluir/<int:pk>', views.DeleteOSView.as_view(), name = 'cliente/OS/excluir'),
    path('OS/lista/<int:id>', views.ListOSView.as_view(), name = 'cliente/OS/lista'),
    path('editar/<int:id>', CadastroClienteWizard.as_view(create_cliente_forms), name = 'cliente/editar'),
    path('', views.appMenu, name = 'cliente/menu'),
    # API
    path('OS/api/load-employees/', views.filterEmployeeDropDown, name = 'cliente/OS/loadEmployees'),
    path('OS/lista/excluir-brancos/<int:id>', views.deleteBlankOS, name = 'cliente/OS/lista/excluir-brancos'),
    path('api/get_by_name/', views.autocompleteByname, name = 'cliente/autocompleteByName')
    ]
