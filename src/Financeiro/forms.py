from django import forms
from .models import Entrada, Saida, Balanco
from Cliente.models import BasicInfo as ClientBasicInfo
from django.forms import widgets

class EntradaForm(forms.ModelForm):
    class Meta():
        model   =   Entrada

        fields  =   [
            'cliente',
            'classificacao_receita',
            'produto',
            'quantidade_produto',
            'valor',
            'percentual_desconto',
            'forma_pagamento',
            'data_vencimento',
            'receita_fixa',
            'observacao'
        ]

        labels  =   {
            'cliente'                   :   'Cliente',
            'classificacao_receita'     :   'Classificação da Receita',
            'produto'                   :   'Produto',
            'quantidade_produto'        :   'Quantidade',
            'valor'                     :   'Valor',
            'percentual_desconto'       :   'Desconto Percentual',
            'forma_pagamento'           :   'Forma de Pagamento',
            'data_vencimento'           :   'Data de Vencimento',
            'receita_fixa'              :   'Receita Fixa',
            'observacao'                :   'Observação'
        }

        widgets =   {
            'classificacao_receita'     :   widgets.TextInput,
            'produto'                   :   widgets.TextInput,
            'quantidade_produto'        :   widgets.TextInput,
            'valor'                     :   widgets.TextInput,
            'percentual_desconto'       :   widgets.TextInput,
            'data_vencimento'           :   widgets.DateInput,
            'receita_fixa'              :   widgets.CheckboxInput,
            'observacao'                :   widgets.Textarea
        }
    
    def __init__(self, *args, **kwargs):
        super(EntradaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = ClientBasicInfo.objects.all()
        self.fields['cliente'].label_from_instance = lambda obj: "%s %s" % (obj.primeiro_nome, obj.ultimo_nome)

class SaidaForm(forms.ModelForm):
    class Meta():
        model   =   Saida

        fields  =   [
            'classificacao_despesa',
            'produto',
            'quantidade_produto',
            'valor',
            'percentual_desconto',
            'forma_pagamento',
            'data_vencimento',
            'despesa_fixa',
            'observacao'
        ]

        labels  =   {
            'classificacao_despesa'     :   'Classificação da Despesa',
            'produto'                   :   'Produto',
            'quantidade_produto'        :   'Quantidade',
            'valor'                     :   'Valor',
            'percentual_desconto'       :   'Desconto Percentual',
            'forma_pagamento'           :   'Forma de Pagamento',
            'data_vencimento'           :   'Data de Vencimento',
            'despesa_fixa'              :   'Despesa Fixa',
            'observacao'                :   'Observação'
        }

        widgets =   {
            'classificacao_despesa'     :   widgets.TextInput,
            'produto'                   :   widgets.TextInput,
            'quantidade_produto'        :   widgets.TextInput,
            'valor'                     :   widgets.TextInput,
            'percentual_desconto'       :   widgets.TextInput,
            'data_vencimento'           :   widgets.DateInput,
            'despesa_fixa'              :   widgets.CheckboxInput,
            'observacao'                :   widgets.Textarea
        }
