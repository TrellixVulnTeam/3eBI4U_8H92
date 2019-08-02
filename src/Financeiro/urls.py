from django.urls import path
from . import views    


urlpatterns = [
    path('fatura/', views.FaturaOSSelectionView.as_view(), name = 'financeiro/fatura/selecionarOS'),
    path('fatura/criar/<str:os>', views.FaturaCreationView.as_view(), name = 'financeiro/fatura/criar'),
    path('', views.financeiroMenu.as_view(), name = 'financeiro/appMenu'),
    
    # API URLS
    path('api/listaOS/', views.listaClientes, name = 'financeiro/api/listaOS'),
    ]
