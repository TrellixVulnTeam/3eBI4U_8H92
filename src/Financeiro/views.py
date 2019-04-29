from django.shortcuts import render, redirect
from .forms import EntradaForm, SaidaForm
from .models import Entrada, Saida, Balanco, LancamentosFixos
from Cliente.models import BasicInfo
from django.utils import timezone
from decimal import Decimal
from .utilities import getLastInputs
from .tables import FinancialMovementTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


# Create your views here.

@login_required
def lancamentosReceita(request, *args, **kwargs):

        template_name = "income.html"
        context = {
                'form' : EntradaForm(),
        }

        filledform = EntradaForm(request.POST)
        if filledform.is_valid():

                savingform = filledform.save(commit = False)
                savingform.datahora_registro = timezone.localtime(timezone.now())
                data_vencimento = savingform.data_vencimento
                savingform.save()        
                
                # UPDATE AND LOG ACCOUNT BALANCE
                lastbalance  = Balanco.objects.all().latest('id').balanco
                lastmovement = savingform.valor
                lastmovement = Decimal(lastmovement.replace('.', '').replace(',', '.'))
                newbalance   = lastbalance + lastmovement
                
                newbalanceobj                       = Balanco()
                newbalanceobj.datahora_registro     = timezone.localtime(timezone.now())
                newbalanceobj.balanco               = newbalance
                newbalanceobj.save()

                # UPDATE NEW FIX INCOME
                if 'receita_fixa' in request.POST: 
                        if request.POST['receita_fixa'] == 'on':
                                newfixobj       =       LancamentosFixos()
                                newfixobj.valor = request.POST['valor']
                                newfixobj.flag_receita = True
                                newfixobj.data_vencimento_inicial = data_vencimento

                                if request.POST['periodicidade'] == '1':
                                        newfixobj.periodicidade_diaria = True
                                if request.POST['periodicidade'] == '2':
                                        newfixobj.periodicidade_semanal = True
                                if request.POST['periodicidade'] == '3':
                                        newfixobj.periodicidade_quinzenal = True
                                if request.POST['periodicidade'] == '4':
                                        newfixobj.periodicidade_mensal = True
                                if request.POST['periodicidade'] == '5':
                                        newfixobj.periodicidade_trimestral = True
                                if request.POST['periodicidade'] == '6':
                                        newfixobj.periodicidade_semestral = True
                                if request.POST['periodicidade'] == '7':
                                        newfixobj.periodicidade_anual = True
                                newfixobj.save()

                return HttpResponse("TESTE")
        return render(request, template_name, context)

@login_required
def lancamentosDespesa(request, *args, **kwargs):
        
        
        template_name = "expense.html"
        context = {
                'formExpense' : SaidaForm(),
        }

        filledform = SaidaForm(request.POST)

        
        if filledform.is_valid():

                savingform = filledform.save(commit = False)
                savingform.datahora_registro = timezone.localtime(timezone.now())
                data_vencimento = savingform.data_vencimento
                savingform.save()        
                
                # UPDATE AND LOG ACCOUNT BALANCE
                lastbalance  = Balanco.objects.all().latest('id').balanco
                lastmovement = savingform.valor
                lastmovement = Decimal(lastmovement.replace('.', '').replace(',', '.'))
                newbalance   = lastbalance - lastmovement
                
                newbalanceobj                       = Balanco()
                newbalanceobj.datahora_registro     = timezone.localtime(timezone.now())
                newbalanceobj.balanco               = newbalance
                newbalanceobj.save()

                # UPDATE NEW FIX EXPENSE 
                if 'despesa_fixa' in request.POST:
                        if request.POST['despesa_fixa'] == 'on':
                                newfixobj       =       LancamentosFixos()
                                newfixobj.valor = request.POST['valor']
                                newfixobj.flag_despesa = True
                                newfixobj.data_vencimento_inicial = data_vencimento

                                if request.POST['periodicidade'] == '1':
                                        newfixobj.periodicidade_diaria = True
                                if request.POST['periodicidade'] == '2':
                                        newfixobj.periodicidade_semanal = True
                                if request.POST['periodicidade'] == '3':
                                        newfixobj.periodicidade_quinzenal = True
                                if request.POST['periodicidade'] == '4':
                                        newfixobj.periodicidade_mensal = True
                                if request.POST['periodicidade'] == '5':
                                        newfixobj.periodicidade_trimestral = True
                                if request.POST['periodicidade'] == '6':
                                        newfixobj.periodicidade_semestral = True
                                if request.POST['periodicidade'] == '7':
                                        newfixobj.periodicidade_anual = True
                                newfixobj.save()


                return redirect(appMenuFinanceiro)
        return render(request, template_name, context)
        
@login_required
def lancamentosFinanceiro(request, *args, **kwargs):

        # Creating List Variables from Models 
        data = []

        cliente                         =       list(Entrada.objects.values_list('cliente', flat = True))
        cliente                         =       [BasicInfo.objects.get(id = c).primeiro_nome + ' ' + BasicInfo.objects.get(id = c).ultimo_nome for c in cliente]
        classificacao_receita           =       list(Entrada.objects.values_list('classificacao_receita', flat = True)) 
        classificacao_despesa           =       list(Saida.objects.values_list('classificacao_despesa', flat = True))
        produto_receita                 =       list(Entrada.objects.values_list('produto', flat = True)) 
        produto_despesa                 =       list(Saida.objects.values_list('produto', flat = True))
        quantidade_produto_receita      =       list(Entrada.objects.values_list('quantidade_produto', flat = True)) 
        quantidade_produto_despesa      =       list(Saida.objects.values_list('quantidade_produto', flat = True))
        valor_receita                   =       list(Entrada.objects.values_list('valor', flat = True)) 
        valor_despesa                   =       list(Saida.objects.values_list('valor', flat = True))
        percentual_desconto_receita     =       list(Entrada.objects.values_list('percentual_desconto', flat = True)) 
        percentual_desconto_despesa     =       list(Saida.objects.values_list('percentual_desconto', flat = True))
        forma_pagamento_receita         =       list(Entrada.objects.values_list('forma_pagamento', flat = True)) 
        forma_pagamento_despesa         =       list(Saida.objects.values_list('forma_pagamento', flat = True))
        data_vencimento_receita         =       list(Entrada.objects.values_list('data_vencimento', flat = True))
        data_vencimento_despesa         =       list(Saida.objects.values_list('data_vencimento', flat = True))
        fixa_receita                    =       list(Entrada.objects.values_list('receita_fixa', flat = True)) 
        fixa_despesa                    =       list(Saida.objects.values_list('despesa_fixa', flat = True))
        observacao_receita              =       list(Entrada.objects.values_list('observacao', flat = True)) 
        observacao_despesa              =       list(Saida.objects.values_list('observacao', flat = True))
        datahora_registro_receita       =       list(Entrada.objects.values_list('datahora_registro', flat = True)) 
        datahora_registro_despesa       =       list(Saida.objects.values_list('datahora_registro', flat = True))

        # Appending Incomes to Table
        for value in range(len(cliente)):
                data_dict = {}
                                
                data_dict['cliente']                    =       cliente.pop(0)
                data_dict['classificacao']              =       classificacao_receita.pop(0)   
                data_dict['produto']                    =       produto_receita.pop(0)
                data_dict['quantidade_produto']         =       quantidade_produto_receita.pop(0)
                data_dict['valor']                      =       valor_receita.pop(0)
                data_dict['percentual_desconto']        =       percentual_desconto_receita.pop(0)
                data_dict['forma_pagamento']            =       forma_pagamento_receita.pop(0)
                data_dict['data_vencimento']            =       data_vencimento_receita.pop(0)
                data_dict['fixa']                       =       fixa_receita.pop(0)
                data_dict['observacao']                 =       observacao_receita.pop(0)
                data_dict['datahora_registro']          =       datahora_registro_receita.pop(0)

                data.append(data_dict)
        
        # Appending Expense to Table
        for value in range(len(classificacao_despesa)):
                data_dict = {}
                                
                data_dict['cliente']                    =       ''
                data_dict['classificacao']              =       classificacao_despesa.pop(0)   
                data_dict['produto']                    =       produto_despesa.pop(0)
                data_dict['quantidade_produto']         =       quantidade_produto_despesa.pop(0)
                data_dict['valor']                      =       valor_despesa.pop(0)
                data_dict['percentual_desconto']        =       percentual_desconto_despesa.pop(0)
                data_dict['forma_pagamento']            =       forma_pagamento_despesa.pop(0)
                data_dict['data_vencimento']            =       data_vencimento_despesa.pop(0)
                data_dict['fixa']                       =       fixa_despesa.pop(0)
                data_dict['observacao']                 =       observacao_despesa.pop(0)
                data_dict['datahora_registro']          =       datahora_registro_despesa.pop(0)


                data.append(data_dict)

        # Sorting List Data by datahora_registro
        data.sort(key=lambda item:item['datahora_registro'], reverse=True)

        # Instantiating Table Object and Creating Context
        table = FinancialMovementTable(data)
        table.paginate(page=request.GET.get('page', 1), per_page=10)
        template_name   =   'financial_movement.html'
        
        context = {
                'table'         : table,
                }

        return render(request, template_name, context)

@login_required
def appMenuFinanceiro(request, *args, **kwargs):
        form        =   EntradaForm()    
        formExpense =   SaidaForm()

        template_name   =   'app_menu_financeiro.html'

        if request.POST:
                
                if 'expenseform' in request.POST: 
                        
                        filledform = SaidaForm(request.POST)
                        
                        if filledform.is_valid():
                
                                savingform = filledform.save(commit = False)
                                savingform.datahora_registro = timezone.localtime(timezone.now())
                                data_vencimento = savingform.data_vencimento
                                savingform.save()        
                                
                                # UPDATE AND LOG ACCOUNT BALANCE
                                lastbalance  = Balanco.objects.all().latest('id').balanco
                                lastmovement = savingform.valor
                                lastmovement = Decimal(lastmovement.replace('.', '').replace(',', '.'))
                                newbalance   = lastbalance - lastmovement
                                
                                newbalanceobj                       = Balanco()
                                newbalanceobj.datahora_registro     = timezone.localtime(timezone.now())
                                newbalanceobj.balanco               = newbalance
                                newbalanceobj.save()

                                # UPDATE NEW FIX EXPENSE 
                                if 'despesa_fixa' in request.POST:
                                        if request.POST['despesa_fixa'] == 'on':
                                                newfixobj       =       LancamentosFixos()
                                                newfixobj.valor = request.POST['valor']
                                                newfixobj.flag_despesa = True
                                                newfixobj.data_vencimento_inicial = data_vencimento

                                                if request.POST['periodicidade'] == '1':
                                                        newfixobj.periodicidade_diaria = True
                                                if request.POST['periodicidade'] == '2':
                                                        newfixobj.periodicidade_semanal = True
                                                if request.POST['periodicidade'] == '3':
                                                        newfixobj.periodicidade_quinzenal = True
                                                if request.POST['periodicidade'] == '4':
                                                        newfixobj.periodicidade_mensal = True
                                                if request.POST['periodicidade'] == '5':
                                                        newfixobj.periodicidade_trimestral = True
                                                if request.POST['periodicidade'] == '6':
                                                        newfixobj.periodicidade_semestral = True
                                                if request.POST['periodicidade'] == '7':
                                                        newfixobj.periodicidade_anual = True
                                                newfixobj.save()


                                return redirect(appMenuFinanceiro)
        
        lastTransactions = getLastInputs(Entrada.objects.all().reverse(), Saida.objects.all().reverse())
        idx = 0
        lastTransactionsDict = {}

        for item in lastTransactions:
                lastTransactionsDict['input_' + str(idx)] = item
                idx += 1    

        context = {
                'form' : form,
                'formExpense' : formExpense,
                'obj_balancoatual' : Balanco.objects.all().latest('id'),
                **lastTransactionsDict
                }
                
        return render(request, template_name, context)

@login_required
def fluxoFinanceiro(request, *args, **kwargs):
        template_name = 'financial_flow.html'
        
        # Getting Time Logs from Incomes and Expenses Tables
        years_log = list(set([x.year for x in Entrada.objects.values_list('datahora_registro', flat = True)] + [x.year for x in Saida.objects.values_list('datahora_registro', flat = True)]))
        months_log = list(set([x.month for x in Entrada.objects.values_list('datahora_registro', flat = True)] + [x.month for x in Saida.objects.values_list('datahora_registro', flat = True)]))
        
        # Creating Base Context
        context = {
                'years' : years_log,
                'months': months_log
                }

        # Getting Daily Income and Expense
        if request.GET:
                if 'month' in request.GET:
                        month = request.GET.get('month')
                if 'year' in request.GET:
                        year  = request.GET.get('year')

                if year != '' and month != '':
                        income = Entrada.objects.all()
                        expense = Saida.objects.all()
                        
                        income = [x for x in income if x.datahora_registro.year == int(year) and x.datahora_registro.month == int(month)]
                        expense = [x for x in expense if x.datahora_registro.year == int(year) and x.datahora_registro.month == int(month)]
                        
                        expense_days = [x.datahora_registro.day for x in expense]
                        expense_values = [x.valor for x in expense]

                        income_days = [x.datahora_registro.day for x in income]
                        income_values = [x.valor for x in income]

                        income_pairs = list(zip(income_days, income_values))
                        expense_pairs = list(zip(expense_days, expense_values))

                        income_dict = {}
                        expense_dict = {}

                        for k, v in income_pairs:
                                v = v.replace('.', '').replace(',', '.')
                                k = 'income_' + str(k) 
                                if k not in income_dict.keys():
                                        income_dict[k] = Decimal(v)
                                else:
                                        income_dict[k] += Decimal(v)
                        
                        for k, v in expense_pairs:
                                v = v.replace('.', '').replace(',', '.')
                                k = 'expense_' + str(k) 
                                if k not in expense_dict.keys():
                                        expense_dict[k] = Decimal(v)
                                else:
                                        expense_dict[k] += Decimal(v)

                        context.update({
                                **income_dict,
                                **expense_dict
                                })

                        return render(request, template_name, context)
                else:
                        if month == '':
                                context.update({
                                        'ERROR' : 1,
                                        'ERROR_HEADER' : 'Mês Inváido !',
                                        'ERROR_MESSAGE' : 'Selecione um mês válido.'
                                })
                        elif year == '':
                                context.update({
                                        'ERROR' : 1,
                                        'ERROR_HEAD' : 'Ano Inválido !',
                                        'ERROR_MESSAGE' : 'Selecione um ano válido.'
                                })

        return render(request, template_name, context)