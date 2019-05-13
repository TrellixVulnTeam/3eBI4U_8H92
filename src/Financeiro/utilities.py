from datetime import date
from django.core.exceptions import ValidationError

# Date Validator That Prevents Future Dates
def validateNoFutureDates(value):

        if value > date.today():
                raise ValidationError('Datas Futúras São Inválidas Neste Campo')


def getLastInputs(querysetIncome, querysetExpense):
        QIncome = querysetIncome.order_by('datahora_registro')
        QExpense = querysetExpense.order_by('datahora_registro')
        
        try:
                lastincomes = list(QIncome)[:7]
        except IndexError:
                lastincomes = list(QIncome)
        
        try:
                lastexpenses = list(QExpense)[:7]
        except IndexError:
                lastexpenses = list(QExpense)
        
        resultlist = []

        while len(lastincomes) != 0 and len(lastexpenses) != 0:
                if lastincomes[0].datahora_registro > lastexpenses[0].datahora_registro:
                        lastincome = lastincomes.pop(0)
                        resultlist.append(lastincome)
                else:
                        lastexpense = lastexpenses.pop(0)
                        resultlist.append(lastexpense)
        
        return resultlist


