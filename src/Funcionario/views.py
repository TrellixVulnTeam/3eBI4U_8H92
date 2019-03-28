from django.shortcuts import render, redirect
from .models import (
    BasicInfo,
    AddressInfo,
    DocumentsInfo,
    ContactInfo,
    ForeignerInfo,
    HandicappedInfo,
    BankingInfo,
    AnotherJobInfo,
    InternInfo,
    PositionInfo,
    ContractualInfo,
    DocumentAttachments,
    Dependente
    )
from .forms import (
    BasicInfoForm,
    AddressInfoForm,
    DocumentsInfoForm,
    ForeignerInfoForm,
    HandicappedInfoForm,
    ContactInfoForm,
    BankingInfoForm,
    AnotherJobInfoForm,
    InternInfoForm,
    PositionInfoForm,
    ContractualInfoForm,
    DocScansForm,
    DependenteForm,
    )

def addFuncionarioBasicInfo(request, *args, **kwargs):

    form = BasicInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()

    context = {
        'form'          :  form,
        'btntxt'        :  'Próximo',
        'formaction'    :   '/endereco/',
        'currentpage'   :   '1'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioAddressInfo(request, *args, **kwargs):
    
    form = AddressInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'        

    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioDocumentsInfo(request, *args, **kwargs):
    
    form = DocumentsInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioContactInfoForm(request, *args, **kwargs):
    
    form = ContactInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioHandicappedInfo(request, *args, **kwargs):
    
    form = HandicappedInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioForeignerInfo(request, *args, **kwargs):
    
    form = ForeignerInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioBankingInfo(request, *args, **kwargs):
    
    form = BankingInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioAnotherJobInfo(request, *args, **kwargs):
    
    form = AnotherJobInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioInternInfo(request, *args, **kwargs):
    
    form = InternInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()

    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioPositionInfo(request, *args, **kwargs):
    
    form = PositionInfoForm(request.POST or None)
    
    if form.is_valid():
        form.save()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioContractInfo(request, *args, **kwargs):

    form = ContractualInfoForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form'   :   form,
        'btntxt' :  'Próximo'
    }

    return render(request, 'create_employee_form_template.html', context)

def addFuncionarioDocScans(request, *args, **kwargs):

    form = DocScansForm(request.POST or None)

    if form.is_valid():
        form.save()

    context = {
        'form'   :   form,
        'btntxt' :  'Salvar'
    }

    return render(request, 'create_employee_form_template.html', context)

def addDependente(request, *args, **kwargs):
    
    form = DependenteForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        form = DependenteForm()
    
    context = {
        'form'   :   form,
        'btntxt' :  'Adicionar'
    }

    return render(request, 'create_employee_form_template.html', context)
