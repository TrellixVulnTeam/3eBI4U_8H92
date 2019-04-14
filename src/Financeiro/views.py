from django.shortcuts import render, redirect
from .forms import EntradaForm, SaidaForm
from .models import Entrada, Saida, Balanco
from django.utils import timezone
from decimal import Decimal
from .utilities import getLastInputs

# Create your views here.

def appMenuFinanceiro(request, *args, **kwargs):
        form        =   EntradaForm()    
        formExpense =   SaidaForm()

        template_name   =   'app_menu_financeiro.html'

        if request.POST:

                if 'incomeform' in request.POST: 
                
                        filledform = EntradaForm(request.POST)
                        
                        if filledform.is_valid():
                
                                savingform = filledform.save(commit = False)
                                savingform.datahora_registro = timezone.localtime(timezone.now())
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

                                return redirect(appMenuFinanceiro)
                
                elif 'expenseform' in request.POST: 
                        
                        filledform = SaidaForm(request.POST)
                        
                        if filledform.is_valid():
                
                                savingform = filledform.save(commit = False)
                                savingform.datahora_registro = timezone.localtime(timezone.now())
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

