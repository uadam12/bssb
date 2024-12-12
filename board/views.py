from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from app import render
from app.views import create_view, delete_view, update_view, data_view
from applicant.models import AccountBank
from applicant.filters import AccountFilter
from .filters import BankFilter, LGAFilter
from .models import RegistrationDocument
from .forms import (
    RegistrationDocumentForm,
    Board, BoardForm,
    Bank, BankForm,
    LGA, LGAForm
)


def index(request):
    board = Board.load()
    registration_document = RegistrationDocument.objects.all()
    
    return render(
        request, 'board/index', board=board, registration_document=registration_document
    )

def update(request):
    return update_view(request, BoardForm, Board.load(), 'Update board settings', save_instantly=True)


# Registration Documents
def reg_docuements(request):
    return data_view(
        request, data=RegistrationDocument.objects.all(),
        data_template='board/reg-documents.html',
        table_headers=['S/N', 'Name', 'Is Compulsory', 'Actions'],
        add_url=reverse_lazy('board:create-reg-document'),
        title='Registration Documents'
    )
    
def create_reg_docuement(request):
    return create_view(
        request, form_class=RegistrationDocumentForm, 
        success_url='board:reg-documents', form_header='Create Registration Document'
    )

def update_reg_document(request, id):
    reg_doc = get_object_or_404(RegistrationDocument, id=id)
    
    return update_view(
        request, RegistrationDocumentForm, 
        reg_doc, "Update Registration Document", 
        save_instantly=True
    )

def delete_reg_document(request, id):
    reg_doc = get_object_or_404(RegistrationDocument, id=id)
    
    return delete_view(
        request, reg_doc, "Delete Registration Document"
    )
    
# Banks
def banks(request):
    filter = BankFilter(request.GET, queryset=Bank.objects.all())
    
    return data_view(
        request=request, 
        data=filter.qs, filter_form=filter.form,
        add_url=reverse_lazy('board:create-bank'),
        table_headers=['S/N', "Name", 'Code', 'Actions'],
        data_template='board/banks.html', title='Available Banks',
    )

def accounts(request):
    filter = AccountFilter(request.GET, queryset=AccountBank.objects.all())
 
    return data_view(request=request, 
        data=filter.qs, filter_form=filter.form,
        data_template='board/accounts.html', 
        title='Accounts', add_url=None,
        table_headers=['S/N', "Account Name", 'Account Number', 'Bank', 'Account Holder', 'Actions']
    )

def create_bank(request):
    return create_view(
        request, form_class=BankForm, 
        success_url='board:banks', form_header='Create Bank'
    )

def update_bank(request, code):
    bank = get_object_or_404(Bank, code=code)
    
    return update_view(
        request, instance=bank, 
        form_class=BankForm, 
        form_header='Update Bank'
    )
    
def delete_bank(request, code):
    bank = get_object_or_404(Bank, code=code)
    return delete_view(request, model=bank, header='Delete Bank')

# Local Government Area(LGA)
def lgas(request):
    filter = LGAFilter(request.GET, queryset=LGA.objects.all())
    
    return data_view(
        request=request, 
        data=filter.qs, filter_form=filter.form,
        add_url=reverse_lazy('board:create-lga'),
        data_template='board/lgas.html', 
        title='Local Government Areas',
        table_headers=['S/N', "Name", 'Code', 'Actions']
    )

def create_lga(request):
    return create_view(request, 
        form_header='Create Local Government Area',
        form_class=LGAForm, success_url='board:lgas', 
    )

def update_lga(request, code):
    lga = get_object_or_404(LGA, code=code)
    
    return update_view(
        request, instance=lga, form_class=LGAForm, 
        form_header='Update Local Government Area'
    )
    
def delete_lga(request, code):
    lga = get_object_or_404(LGA, code=code)
    return delete_view(request, model=lga, header='Delete Local Government Area')