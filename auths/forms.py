import re
from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
from django.shortcuts import get_object_or_404
from crispy_forms.layout import Layout, Row, Column
from crispy_forms.bootstrap import PrependedText
from crispy_forms.helper import FormHelper
from app.validators import validate_phone_number
from board.models import LGA
from applicant.models import PersonalInformation
from payment.remita import remita
from users.models import User
from .validators import validate_nin, validate_bvn

class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    nin = forms.CharField(label="National Identification Number", required=True, validators=[validate_nin])
    bvn = forms.CharField(label="Bank Verification Number", required=True, validators=[validate_bvn])
    gender = forms.ChoiceField(choices=PersonalInformation.GENDER)
    date_of_birth = forms.DateField(widget=forms.DateInput({'type': 'date', 'placeholder': 'Select your date of birth'}))
    agreed = forms.BooleanField(
        label='I am sure the information I provided is correct to best of my knowledge.', required=False
    )
    lga = forms.ModelChoiceField(
        label='Local Government Area', 
        queryset=LGA.objects.all(),
        empty_label='Select your local government of origin'
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_agreed(self):
        agreed = self.cleaned_data.get('agreed', False)
        
        if not agreed:
            raise ValidationError(f"Please do confirm the information you are giving us is correct.")
        
        return agreed

    def save(self, _=None):
        user = super().save(commit=False)
        data:dict = self.cleaned_data
        user.is_active = False
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        
        info = PersonalInformation(
            phone_number = self.cleaned_data.get('phone_number'),
            gender = data.get('gender'), user = user,
            date_of_birth = data.get('date_of_birth'),
            nin = data.get('nin'), 
            bvn = data.get('bvn'), 
            local_government_area = data.get('lga')
        )

        user.save()
        info.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs.update({
            'placeholder': 'Enter your firstname.',
            'required': 'required'
        })
        
        self.fields['last_name'].widget.attrs.update({
            'placeholder': 'Enter your lastname.',
            'required': 'required'
        })
        
        self.fields['nin'].widget.attrs.update({
            'placeholder': 'Enter your Nation Identification Number(NIN).',
            'hx-post': reverse('auth:nin'), 'hx-target': '#div_id_nin'
        })
        
        self.fields['bvn'].widget.attrs.update({
            'placeholder': 'Enter your Bank Verification Number(BVN).',
            'hx-post': reverse('auth:bvn'), 'hx-target': '#div_id_bvn'
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address',
            'hx-post': reverse('auth:email'), 
            'hx-target': '#div_id_email',
        })
        
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter your phone number',
            'hx-post': reverse('auth:phone_number'), 
            'hx-target': '#div_id_phone_number',
        })

        self.fields['password1'].widget.attrs['placeholder'] = 'Create a strong password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-2'
            ),
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('phone_number', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-2'
            ),
            Row(
                Column('nin', css_class='form-group col-md-6 mb-0'),
                Column('bvn', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ), 'lga',
            Row(
                Column('gender', css_class='form-group col-md-6 mb-0'),
                Column('date_of_birth', css_class='form-group col-md-6 mb-0'),
                css_class='form-row mb-2'
            ),
            Row(
                Column(
                    PrependedText('password1', mark_safe("<i class='bi bi-lock'></i>")), 
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    PrependedText('password2', mark_safe("<i class='bi bi-lock'></i>")), 
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            'agreed'
        )

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address', widget=forms.EmailInput(attrs={
        'required': True,
        'placeholder': 'Enter your email address here...'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'required': True,
        'placeholder': 'Enter your password here...'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            PrependedText('email', mark_safe("<i class='bi bi-envelope'></i>")),
            PrependedText('password', mark_safe("<i class='bi bi-lock'></i>")),
        )