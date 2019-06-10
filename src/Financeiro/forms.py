from django import forms
from .models import Entrada, Saida, Balanco, EntradaProd, SaidaProd
from Cliente.models import BasicInfo as ClientBasicInfo
from django.forms import widgets, modelformset_factory

class EntradaForm(forms.ModelForm):
    class Meta():
        model   =   Entrada

        fields  =   [
            'cliente',
            'forma_pagamento',
            'identificador_receita',
            'observacao'
        ]

        labels  =   {
            'cliente'                   :   'Cliente',
            'forma_pagamento'           :   'Forma de Pagamento',
            'identificador_receita'     :   'Identificador da Receita',
            'observacao'                :   'Observação'
        }

        widgets =   {
            'observacao'                :   widgets.Textarea
        }
    
    def __init__(self, *args, **kwargs):
        super(EntradaForm, self).__init__(*args, **kwargs)
        self.fields['cliente'].queryset = ClientBasicInfo.objects.all()
        self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nome)

class SaidaForm(forms.ModelForm):
    class Meta():
        model   =   Saida

        fields  =   [
            'forma_pagamento',
            'identificador_despesa',
            'observacao'
        ]

        labels  =   {
            'forma_pagamento'           :   'Forma de Pagamento',
            'identificador_despesa'     :   'Identificador da Despesa',
            'observacao'                :   'Observação'
        }

        widgets =   {
            'observacao'                :   widgets.Textarea
        }

EntradaProdFormSet = modelformset_factory(
    EntradaProd,
    fields  = ['classificacao_receita', 'produto', 'quantidade_produto', 'valor_unitario'],
    labels  = {
        'classificacao_receita' : 'Classificação', 
        'produto' : 'Produto', 
        'quantidade_produto' : 'Quantidade',
        'valor_unitario' : 'Valor Unitário'
        },

    widgets  = {
        'classificacao_receita' : widgets.TextInput(attrs = {
            'placeholder' : 'Classificação'
            }), 
        'produto' : widgets.TextInput(attrs = {
            'placeholder' : 'Produto'
            }), 
        'quantidade_produto' : widgets.TextInput(attrs = {
            'placeholder' : 'Quantidade'
            }),
        'valor_unitario' : widgets.TextInput(attrs = {
            'placeholder' : 'Valor Unitário'
            })
        },

    extra = 1,
    )

SaidaProdFormSet = modelformset_factory(
    SaidaProd,
    fields  = ['classificacao_despesa', 'produto', 'quantidade_produto', 'valor_unitario'],
    labels  = {
        'classificacao_despesa' : 'Classificação', 
        'produto' : 'Produto', 
        'quantidade_produto' : 'Quantidade',
        'valor_unitario' : 'Valor Unitário'
        },

    widgets  = {
        'classificacao_despesa' : widgets.TextInput(attrs = {
            'placeholder' : 'Classificação'
            }), 
        'produto' : widgets.TextInput(attrs = {
            'placeholder' : 'Produto'
            }), 
        'quantidade_produto' : widgets.TextInput(attrs = {
            'placeholder' : 'Quantidade'
            }),
        'valor_unitario' : widgets.TextInput(attrs = {
            'placeholder' : 'Valor Unitário'
            })
        },

    extra = 1
    )

