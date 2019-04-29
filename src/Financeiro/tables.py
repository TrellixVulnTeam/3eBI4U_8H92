from django_tables2 import tables, TemplateColumn
from .models import Entrada, Saida
        
class FinancialMovementTable(tables.Table):
    
    # Columns
    
    cliente                 =   tables.columns.Column()
    classificacao           =   tables.columns.Column(verbose_name = "Classificação")
    produto                 =   tables.columns.Column()
    quantidade_produto      =   tables.columns.Column(verbose_name = "Qtd. Produtos")
    valor                   =   tables.columns.Column(verbose_name = "Valor (R$)")
    percentual_desconto     =   tables.columns.Column(verbose_name = "Pct. Desconto (%)")
    forma_pagamento         =   tables.columns.Column(verbose_name = "Forma de Pagamento")
    data_vencimento         =   tables.columns.DateColumn(verbose_name = "Data de Vencimento")
    fixa                    =   tables.columns.BooleanColumn()
    observacao              =   tables.columns.Column(verbose_name = "Observação")
    datahora_registro       =   tables.columns.DateTimeColumn(verbose_name = "Data/Hora de Registo")