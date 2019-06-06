from django.shortcuts import render, redirect, HttpResponse
from .forms import EntradaForm, SaidaForm, EntradaProdFormSet, SaidaProdFormSet
from .models import Entrada, Saida, Balanco, LancamentosFixos, EntradaProd, SaidaProd
from Cliente.models import BasicInfo
from django.utils import timezone
from decimal import Decimal
from .utilities import getLastInputs
from .tables import FinancialMovementTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView
from django.db import transaction
from django.urls import reverse_lazy
import locale


# Create your views here.

@login_required
def lancamentosReceita(request, *args, **kwargs):

        template_name = "income.html"
        context = {
                'form' : EntradaForm(),
        }

        if request.is_ajax():
                filledform = EntradaForm(request.POST)
                if filledform.is_valid():

                        savingform = filledform.save(commit = False)
                        savingform.datahora_registro = timezone.localtime(timezone.now())
                        data_vencimento = savingform.data_vencimento
                        savingform.save()
                        
                        # LOG FIX INCOME IN SESSION
                        if 'receita_fixa' in request.POST:
                                if request.POST['receita_fixa'] == 'on':
                                        request.session['receita_fixa'] = True
                                        request.session['periodicidade'] = request.POST['periodicidade']
                                        request.session['data_vencimento'] = str(data_vencimento)
                                        request.session['identificador_lancamento'] = request.POST['identificador_receita']
                                        request.session['observacao'] = request.POST['observacao']

                        id_venda = Entrada.objects.latest('id').id
                        request.session['id_venda'] = id_venda
                        

                        return redirect(lancamentosReceitaProd)
        return render(request, template_name, context)

@login_required
def lancamentosReceitaProd(request, *args, **kwargs):
        template_name = 'income_prod.html'
        heading_message = 'Lançamento de Produtos'

        if request.method == 'GET' and request.is_ajax():
                formset = EntradaProdFormSet(queryset = EntradaProd.objects.none())
                return render(request, template_name, {
                        'formset' : formset,
                        'heading_message' : heading_message,
                        })
        elif request.method == 'POST':
                
                formset = EntradaProdFormSet(request.POST)
                for form in formset:
                        
                        
                        if form.is_valid():
                                if form.cleaned_data.get('classificacao_receita'):
                                        EntradaObj = Entrada.objects.filter(id = request.session.get('id_venda'))[0]
                                        EntradaObj.valor = request.POST.get('totalValue')
                                        EntradaObj.percentual_desconto = request.POST.get('discount')
                                        EntradaObj.save()

                                        savingform = form.save(commit = False)

                                        savingform.id_entrada = Entrada.objects.filter(id = request.session.get('id_venda'))[0]
                                        savingform.save()

                # UPDATE AND LOG ACCOUNT BALANCE
                lastbalance  = Balanco.objects.all().latest('id').balanco
                lastmovement = request.POST.get('totalValue')
                lastmovement = Decimal(lastmovement)
                newbalance   = lastbalance + lastmovement

                newbalanceobj                       = Balanco()
                newbalanceobj.datahora_registro     = timezone.localtime(timezone.now())
                newbalanceobj.balanco               = newbalance
                newbalanceobj.save()

                # UPDATE NEW FIX INCOME
                if 'receita_fixa' in request.session:
                        if request.session.get('receita_fixa') == True:
                                data_vencimento = request.session.get('data_vencimento')
                                
                                newfixobj       =       LancamentosFixos()
                                newfixobj.valor = request.POST.get('totalValue')
                                newfixobj.flag_receita = True
                                newfixobj.data_vencimento_inicial = data_vencimento
                                newfixobj.identificador_lancamento = request.session.get('identificador_lancamento')
                                newfixobj.observacao = request.session.get('observacao')


                                if request.session['periodicidade'] == '1':
                                        newfixobj.periodicidade_diaria = True
                                if request.session['periodicidade'] == '2':
                                        newfixobj.periodicidade_semanal = True
                                if request.session['periodicidade'] == '3':
                                        newfixobj.periodicidade_quinzenal = True
                                if request.session['periodicidade'] == '4':
                                        newfixobj.periodicidade_mensal = True
                                if request.session['periodicidade'] == '5':
                                        newfixobj.periodicidade_trimestral = True
                                if request.session['periodicidade'] == '6':
                                        newfixobj.periodicidade_semestral = True
                                if request.session['periodicidade'] == '7':
                                        newfixobj.periodicidade_anual = True
                                newfixobj.save()





                return redirect(appMenuFinanceiro)
        return redirect(appMenuFinanceiro)

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
                

                # LOG FIX INCOME IN SESSION
                if 'despesa_fixa' in request.POST:
                        if request.POST['despesa_fixa'] == 'on':
                                request.session['despesa_fixa'] = True
                                request.session['periodicidade'] = request.POST['periodicidade']
                                request.session['data_vencimento'] = str(data_vencimento)
                                request.session['identificador_lancamento'] = request.POST['identificador_despesa']
                                request.session['observacao'] = request.POST['observacao']


                id_venda = Saida.objects.latest('id').id
                request.session['id_venda'] = id_venda


                return redirect(lancamentosDespesaProd)
        return render(request, template_name, context)

@login_required
def lancamentosDespesaProd(request, *args, **kwargs):
        template_name = 'expense_prod.html'
        heading_message = 'Lançamento de Produtos'

        if request.method == 'GET' and request.is_ajax():
                formset = SaidaProdFormSet(queryset = SaidaProd.objects.none())
                return render(request, template_name, {
                        'formset' : formset,
                        'heading_message' : heading_message,
                        })
        elif request.method == 'POST':
                formset = SaidaProdFormSet(request.POST)
                for form in formset:
                        if form.is_valid():
                                if form.cleaned_data.get('classificacao_despesa'):
                                        SaidaObj = Saida.objects.filter(id = request.session.get('id_venda'))[0]
                                        SaidaObj.valor = request.POST.get('totalValue')
                                        SaidaObj.percentual_desconto = request.POST.get('discount')
                                        SaidaObj.save()

                                        savingform = form.save(commit = False)

                                        savingform.id_saida = Saida.objects.filter(id = request.session.get('id_venda'))[0]
                                        savingform.save()

                # UPDATE NEW FIX EXPENSE 
                if 'despesa_fixa' in request.session:
                        if request.session.get('despesa_fixa') == True:
                                data_vencimento = request.session.get('data_vencimento')

                                newfixobj       =       LancamentosFixos()
                                newfixobj.valor = request.POST['totalValue']
                                newfixobj.flag_receita = False
                                newfixobj.flag_despesa = True
                                newfixobj.data_vencimento_inicial = data_vencimento
                                newfixobj.identificador_lancamento = request.session.get('identificador_lancamento')
                                newfixobj.observacao = request.session.get('observacao')                                

                                if request.session['periodicidade'] == '1':
                                        newfixobj.periodicidade_diaria = True
                                if request.session['periodicidade'] == '2':
                                        newfixobj.periodicidade_semanal = True
                                if request.session['periodicidade'] == '3':
                                        newfixobj.periodicidade_quinzenal = True
                                if request.session['periodicidade'] == '4':
                                        newfixobj.periodicidade_mensal = True
                                if request.session['periodicidade'] == '5':
                                        newfixobj.periodicidade_trimestral = True
                                if request.session['periodicidade'] == '6':
                                        newfixobj.periodicidade_semestral = True
                                if request.session['periodicidade'] == '7':
                                        newfixobj.periodicidade_anual = True
                                newfixobj.save()

                # UPDATE AND LOG ACCOUNT BALANCE
                lastbalance  = Balanco.objects.all().latest('id').balanco
                lastmovement = request.POST.get('totalValue')
                lastmovement = Decimal(lastmovement)
                newbalance   = lastbalance - lastmovement
                
                newbalanceobj                       = Balanco()
                newbalanceobj.datahora_registro     = timezone.localtime(timezone.now())
                newbalanceobj.balanco               = newbalance
                newbalanceobj.save()


                return redirect(appMenuFinanceiro)
        return redirect(appMenuFinanceiro)

@login_required
def lancamentosFinanceiro(request, *args, **kwargs):

        # Creating List Variables from Models 
        data = []

        cliente                         =       list(Entrada.objects.values_list('cliente', flat = True))
        cliente                         =       [BasicInfo.objects.get(id = c).nome  for c in cliente]
        identificador_receita           =       list(Entrada.objects.values_list('identificador_receita', flat = True))
        identificador_despesa           =       list(Saida.objects.values_list('identificador_despesa', flat = True))
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
                data_dict['identificador']              =       identificador_receita.pop(0)
                data_dict['valor']                      =       valor_receita.pop(0)
                data_dict['percentual_desconto']        =       percentual_desconto_receita.pop(0)
                data_dict['forma_pagamento']            =       forma_pagamento_receita.pop(0)
                data_dict['data_vencimento']            =       data_vencimento_receita.pop(0)
                data_dict['fixa']                       =       fixa_receita.pop(0)
                data_dict['observacao']                 =       observacao_receita.pop(0)
                data_dict['datahora_registro']          =       datahora_registro_receita.pop(0)

                data.append(data_dict)
        
        # Appending Expense to Table
        for value in range(len(identificador_despesa)):
                data_dict = {}
                                
                data_dict['cliente']                    =       ''
                data_dict['identificador']              =       identificador_despesa.pop(0)   
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

                        total_income_per_day = {}
                        for key, value in income_pairs:
                                total_income_per_day[key] = total_income_per_day.get(key, Decimal(0)) + Decimal(value)
                        
                        total_expense_per_day = {}
                        for key, value in expense_pairs:
                                total_expense_per_day[key] = total_expense_per_day.get(key, Decimal(0)) + Decimal(value)
                        
                        total_per_day = {}
                        if len(total_income_per_day) > len(total_expense_per_day):
                                for key, value in total_income_per_day.items():
                                        total_per_day[key] = total_income_per_day.get(key, Decimal(0)) + total_expense_per_day.get(key, Decimal(0))
                        else:
                                for key, value in total_expense_per_day.items():
                                        total_per_day[key] = total_income_per_day.get(key, Decimal(0)) + total_income_per_day.get(key, Decimal(0))

                        income_dict = {}
                        expense_dict = {}

                        for k, v in income_pairs:
                                k = 'income_' + str(k) 
                                if k not in income_dict.keys():
                                        try:
                                                income_dict[k] = Decimal(v)
                                        except:
                                                income_dict[k] = Decimal('0.0')
                                else:
                                        try:
                                                income_dict[k] += Decimal(v)
                                        except:
                                                income_dict[k] += Decimal('0.0')
                        for k, v in expense_pairs:
                                k = 'expense_' + str(k) 
                                if k not in expense_dict.keys():
                                        expense_dict[k] = Decimal(v)
                                else:
                                        expense_dict[k] += Decimal(v)

                        total_per_day = {'total_' + str(key): total_per_day.get(key) for key in total_per_day.keys()}


                        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

                        for k, v in income_dict.items():
                                income_dict[k] = locale.currency(v, grouping = True, symbol = None)
                        for k, v in expense_dict.items():
                                expense_dict[k] = locale.currency(v, grouping = True, symbol = None)
                        for k, v in total_per_day.items():
                                total_per_day[k] = locale.currency(v, grouping = True, symbol = None)

                        # Calculating Totals

                        totalincome = sum(map(Decimal, map(lambda s: s.replace('.', '').replace(',', '.'), income_dict.values())))
                        totalexpense = sum(map(Decimal, map(lambda s: s.replace('.', '').replace(',', '.'), expense_dict.values())))
                        finaltotal = totalincome - totalexpense

                        totalincome = locale.currency(totalincome, grouping = True, symbol = None)
                        totalexpense = locale.currency(totalexpense, grouping = True, symbol = None)
                        finaltotal = locale.currency(finaltotal, grouping = True, symbol = None)

                        context.update({
                                **income_dict,
                                **expense_dict,
                                **total_per_day
                        })
                        context.update({
                                'total_income' : totalincome,
                                'total_expense' : totalexpense,
                                'final_total' : finaltotal
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

@login_required
def appMenuFinanceiro(request, *args, **kwargs):
        form        =   EntradaForm()    
        formExpense =   SaidaForm()

        template_name   =   'app_menu_financeiro.html'
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

        lastTransactions = getLastInputs(Entrada.objects.all().reverse(), Saida.objects.all().reverse())
        idx = 0
        lastTransactionsDict = {}
        lastTransactionsValueDict = {}

        for item in lastTransactions:
                lastTransactionsDict['input_' + str(idx)] = item
                lastTransactionsValueDict['input_' + str(idx) + '_value'] = locale.currency(Decimal(item.valor), grouping = True, symbol = None)
                idx += 1    
        
        obj_balancoatual = locale.currency(Balanco.objects.all().latest('id').balanco, grouping = True, symbol = None)

        context = {
                'form' : form,
                'formExpense' : formExpense,
                'obj_balancoatual' : obj_balancoatual,
                **lastTransactionsDict,
                **lastTransactionsValueDict,
                }

        return render(request, template_name, context)

@login_required
def deleteRecord(request, *args, **kwargs):
        mov_type        = kwargs.pop('mt', False)
        pk              = kwargs.pop('id', False)
        
        print(pk)
        
        return HttpResponse('OK')
        
        '''
        if not mov_type or not pk:
                return HttpResponse("ERROR 1 - MISSING ARGUMENTS")

        if mov_type == 1:
                entry = Entrada.objects.filter(id = pk)
                lastmovement = id.valor
                entry.delete()  
        elif mov_type == 2:
                entry = Saida.objects.filter(id = pk)
                lastmovement = id.valor
                entry.delete()  


        # UPDATE AND LOG ACCOUNT BALANCE
        lastbalance  = Balanco.objects.all().latest('id').balanco
        lastmovement = Decimal(lastmovement)
        newbalance   = lastbalance - lastmovement
        
        newbalanceobj                       = Balanco()
        newbalanceobj.datahora_registro     = timezone.localtime(timezone.now())
        newbalanceobj.balanco               = newbalance
        newbalanceobj.save()

        return HttpResponse("OK" + str(mov_type) + "-" + str(pk) + " DELETED")
        '''
        