from django.db import models
from Cliente.models import BasicInfo

# CHOICE LISTS

payment_method_choices  =   [('Débito', 'Cartão de Débito'), ('Crédito', 'Cartão de Crédito'), ('Boleto', 'Boleto'), ('Depósito', 'Depósito'), ('Transferência', 'Transferência'), ('Dinheiro', 'Dinheiro')]

# Create your models here.
class Entrada(models.Model):
    
    id                      =   models.BigAutoField(primary_key = True)

    cliente                 =   models.ForeignKey(BasicInfo, on_delete=models.CASCADE)
    
    valor                   =   models.CharField(max_length = 20, null = True, blank = True)
    percentual_desconto     =   models.CharField(max_length = 5, null = True, blank = True)
    forma_pagamento         =   models.CharField(max_length = 100, choices = payment_method_choices)    

    identificador_receita   =   models.CharField(max_length = 100)
    observacao              =   models.CharField(max_length = 500, null = True, blank = True)
    
    datahora_registro       =   models.DateTimeField()

class EntradaProd(models.Model):

    id_entrada              =   models.ForeignKey(Entrada, on_delete=models.CASCADE, related_name="products")
    
    classificacao_receita   =   models.CharField(max_length = 100)
    produto                 =   models.CharField(max_length = 100)
    quantidade_produto      =   models.CharField(max_length = 100)
    valor_unitario          =   models.CharField(max_length = 20)

class Saida(models.Model):

    id                      =   models.BigAutoField(primary_key = True)
    
    valor                   =   models.CharField(max_length = 20, null = True, blank = True)
    percentual_desconto     =   models.CharField(max_length = 5, null = True, blank = True)
    forma_pagamento         =   models.CharField(max_length = 100, choices = payment_method_choices)    

    identificador_despesa   =   models.CharField(max_length = 100)
    observacao              =   models.CharField(max_length = 100, null = True, blank = True)

    datahora_registro       =   models.DateTimeField()

class SaidaProd(models.Model):
    
    id_saida = models.ForeignKey(Saida, on_delete = models.CASCADE, related_name = 'expense_produts')

    classificacao_despesa   =   models.CharField(max_length = 100)
    produto                 =   models.CharField(max_length = 100)
    quantidade_produto      =   models.CharField(max_length = 100)
    valor_unitario          =   models.CharField(max_length = 20)

class Balanco(models.Model):

    id                      =   models.BigAutoField(primary_key = True)

    datahora_registro       =   models.DateTimeField()
    balanco                 =   models.DecimalField(max_digits = 17, decimal_places = 2)

class LancamentosFixos(models.Model):

    flag_receita                    =   models.BooleanField(null = True, blank = True)
    flag_despesa                    =   models.BooleanField(null = True, blank = True)

    periodicidade_diaria            =   models.BooleanField(null = True, blank = True)
    periodicidade_semanal           =   models.BooleanField(null = True, blank = True)
    periodicidade_quinzenal         =   models.BooleanField(null = True, blank = True)
    periodicidade_mensal            =   models.BooleanField(null = True, blank = True)
    periodicidade_trimestral        =   models.BooleanField(null = True, blank = True)
    periodicidade_semestral         =   models.BooleanField(null = True, blank = True)
    periodicidade_anual             =   models.BooleanField(null = True, blank = True)

    # INFO NEEDED TO MAKE FINANCIAL RELEASES

    valor                           =   models.CharField(max_length = 20)
    data_vencimento_inicial         =   models.DateField()
    identificador_lancamento        =   models.CharField(max_length = 100)
    observacao                      =   models.CharField(max_length = 500, null = True, blank = True)
