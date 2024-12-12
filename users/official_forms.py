from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit, Div
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter lastname'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email address'
        
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            Div(
                Submit('save', 'Save User'),
                css_class='text-end'
            )
        )
    

    def save(self, commit=True) -> User:
        user:User = super().save(commit=False)
        user.set_password('bssb@123')
        if commit: user.save()
        
        return user

class OfficialForm(forms.ModelForm):
    is_admin = forms.BooleanField(help_text='Check if the official is an adminstrator', required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs = {
            'placeholder': 'Enter official firstname',
        }
        
        self.fields['last_name'].widget.attrs = {
            'placeholder': 'Enter official lastname',
        }
        
        self.fields['email'].widget.attrs = {
            'placeholder': 'Enter official email address',
        }

    def save(self, commit=True):
        user:User = super().save(commit=False)
        user.access_code = 3
        if commit: user.save()
        
        if commit is True: 
            if not user.password:
                user.set_password('bssb@123')
            
            access_code = 3 if self.cleaned_data['is_admin'] else 2
            user.access_code = access_code
            user.save()
        
        return user

class GuestForm(UserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.access_code = 2
        if commit: user.save()
        
        return user