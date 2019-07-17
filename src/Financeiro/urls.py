from django.urls import path
from . import views    


urlpatterns = [
    path('fatura/', views.GerarFatura.as_view(), name = 'financeiro/fatura'),
    path('api/listaOS/', views.ListaOS, name = 'financeiro/api/listaOS'),
    path('api/geraFatura/', views.GeraFatura, name = 'financeiro/api/geraFatura'),
    ]
