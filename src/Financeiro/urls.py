from django.urls import path
from .views import appMenuFinanceiro, lancamentosFinanceiro, fluxoFinanceiro, lancamentosReceita, lancamentosDespesa

urlpatterns = [
    path('', appMenuFinanceiro, name = 'financeiro/menu'),
    path('lancamentos/', lancamentosFinanceiro, name = 'financeiro/lancamentos'),
    path('fluxo/', fluxoFinanceiro, name = 'financeiro/fluxo'),
    path('lancamento-receita/', lancamentosReceita, name = 'lancamentosReceita'),
    path('lancamento-despesa/', lancamentosDespesa, name = 'lancamentosDespesa'),
]