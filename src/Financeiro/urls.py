from django.urls import path
from . import views

urlpatterns = [
    path('', views.appMenuFinanceiro, name = 'financeiro/menu'),
    path('lancamentos/', views.lancamentosFinanceiro, name = 'financeiro/lancamentos'),
    path('fluxo/', views.fluxoFinanceiro, name = 'financeiro/fluxo'),
    path('lancamento-receita/', views.lancamentosReceita, name = 'lancamentosReceita'),
    path('lancamento-despesa/', views.lancamentosDespesa, name = 'lancamentosDespesa'),
    path('lancamento-receita-prod', views.lancamentosReceitaProd, name = 'lancamentosReceitaProd' ),
    path('lancamento-despesa-prod', views.lancamentosDespesaProd, name = 'lancamentosDespesaProd' ),
    path('lancamentos/remover-lancamento/byid/<int:id><int:mt>', views.deleteRecord, name = 'deleteMovementRecord')
]