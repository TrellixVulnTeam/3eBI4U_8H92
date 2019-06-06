from django_tables2 import tables, TemplateColumn, utils
from .models import Entrada, Saida


class FinancialMovementTable(tables.Table):
    
    # Columns
    
    cliente                 =   tables.columns.Column()
    identificador           =   tables.columns.Column(verbose_name = "Identificador de Transação")
    valor                   =   tables.columns.Column(verbose_name = "Valor (R$)")
    percentual_desconto     =   tables.columns.Column(verbose_name = "Pct. Desconto (%)")
    forma_pagamento         =   tables.columns.Column(verbose_name = "Forma de Pagamento")
    data_vencimento         =   tables.columns.DateColumn(verbose_name = "Data de Vencimento")
    fixa                    =   tables.columns.BooleanColumn()
    observacao              =   tables.columns.Column(verbose_name = "Observação")
    datahora_registro       =   tables.columns.DateTimeColumn(verbose_name = "Data/Hora de Registo")
    
    #opções                  =   TemplateColumn(template_name = 'financialmovement_table_edit_record.html')
    opções                  =   tables.columns.LinkColumn('deleteRecord', args = [utils.A('pk')], attrs = {'class' : 'btn, btnmenu'})