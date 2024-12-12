from django import forms
from .models import Board, RegistrationDocument, Bank, LGA


class BoardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['motto'].widget.attrs['placeholder'] = 'Enter board motto'
        self.fields['registration_fee'].widget.attrs['placeholder'] = 'Enter registration FEE'
        self.fields['registration_criteria'].widget.attrs['placeholder'] = 'Enter board registration criteria'
        self.fields['about'].widget.attrs['placeholder'] = 'Enter information about the board'
        
    class Meta:
        model = Board
        fields = (
            "motto", "registration_fee", 
            "about", "registration_criteria", 
            "registration_is_open"
        )


class RegistrationDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter document name'
        
    class Meta:
        model = RegistrationDocument
        fields = ("name", "required")


class BankForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter bank name'
        self.fields['code'].widget.attrs['placeholder'] = 'Enter bank code'
        
        
    class Meta:
        model = Bank
        fields = ("name", "code", "is_available")

class LGAForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Enter Local Goverment Area name'
        self.fields['code'].widget.attrs['placeholder'] = 'Enter Local Goverment Area code'

    class Meta:
        model = LGA
        fields = ("name", "code")
