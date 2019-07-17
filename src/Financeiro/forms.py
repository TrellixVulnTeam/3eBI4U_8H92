from django import forms
from Cliente.models import BasicInfo as Cliente

class ClienteListing(forms.Form):
    cliente = forms.ModelChoiceField(Cliente.objects.all())



class Fatura(forms.ModelForm):
    class Meta():
        fields = [
            'cliente',
            'OS',
            'valor_total',
            'desconto',
            'pagamento_efetuado',
            'data_emissao',
            'data_vencimento',
            'data_pagamento'
        ]
