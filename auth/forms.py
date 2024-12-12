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

class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    nin = forms.CharField(label="National Identification Number", max_length=11, min_length=11, required=True)
    bvn = forms.CharField(label="Bank Verification Number", max_length=11, min_length=11, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
    
    def clean_nin(self):
        nin = self.cleaned_data['nin']
        nin_format = r'\d{11}'
        nin_match = re.match(nin_format, nin)
        
        if not nin_match:
            raise ValidationError("Invalid NIN")

        info = PersonalInformation.objects.filter(nin=nin)
        if info.exists():
            raise ValidationError(f"Applicant with this National Identification Number(NIN: {nin}) already exists.")
        
        nin_data = remita.get_nin_data(nin)
        if nin_data.get('stateOfOriginCode') != 'BO':
            raise ValidationError('This program is only applicable to Borno state indigen.')

        self.cleaned_data['nin_data'] = nin_data            
        return nin
    
    def clean_bvn(self):
        bvn = self.cleaned_data['bvn']
        bvn_format = r'\d{11}'
        bvn_match = re.match(bvn_format, bvn)
        
        if not bvn_match:
            raise ValidationError("Invalid BVN")

        info = PersonalInformation.objects.filter(bvn=bvn)
        if info.exists():
            raise ValidationError(f"Applicant with this Bank Verification Number(BVN: {bvn}) already exists.")

        bvn_data = remita.get_bvn_data(bvn)
        if bvn_data.get('stateOfOriginCode') != 'BO':
            raise ValidationError('This program is only applicable to Borno state indigen.')

        self.cleaned_data['bvn_data'] = bvn_data
        return bvn

    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        
        info = PersonalInformation.objects.filter(phone_number=phone_number)
        if info.exists():
            raise ValidationError(f"Applicant with this Phone Number({phone_number}) already exists.")
        
        return phone_number

    def clean(self):
        data = super().clean()

        nin_data = data.get('nin_data', None)
        if not nin_data:
            raise ValidationError('NIN Details not found.')

        bvn_data = data.get('bvn_data', None)
        if not bvn_data:
            raise ValidationError('BVN Details not found.')

        nin_dob, bvn_dob = nin_data.get('dateOfBirth', ''), bvn_data.get('dateOfBirth', '')
        if nin_dob and bvn_dob and nin_dob > bvn_dob:
            raise ValidationError('NIN and BVN date of birth mismatch.')

        return data

    def save(self, _=None):
        user = super().save(commit=False)
        data:dict = self.cleaned_data['nin_data']
        user.is_active = False
        user.first_name = data.get('firstName')
        user.last_name = data.get('lastName')
        lga = get_object_or_404(LGA, pk=data.get('lgaofOriginCode'))

        info = PersonalInformation(
            phone_number = self.cleaned_data.get('phone_number'),
            gender = data.get('gender'), user = user,
            date_of_birth = data.get('dateOfBirth'),
            nin = self.cleaned_data['nin'], 
            bvn = self.cleaned_data['bvn'], 
            local_government_area = lga
        )

        user.save()
        info.save()

        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['nin'].widget.attrs.update({
            'placeholder': 'Enter your Nation Identification Number(NIN).',
            'hx-post': reverse('validate:nin'),
            'hx-triger': 'keyup',
            'hx-target': '#div_id_nin'
        })
        
        self.fields['bvn'].widget.attrs.update({
            'placeholder': 'Enter your Bank Verification Number(BVN).',
            'hx-post': reverse('validate:bvn'),
            'hx-target': '#div_id_bvn'
        })

        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address',
            'hx-post': reverse('validate:email'),
            'hx-target': '#div_id_email',
            'hx-swap': 'outerHTML'
        })
        
        self.fields['phone_number'].widget.attrs.update({
            'placeholder': 'Enter your phone number',
            'hx-post': reverse('validate:phone_number'),
            'hx-target': '#div_id_phone_number',
            'hx-swap': 'outerHTML'
        })
        
        self.fields['password1'].widget.attrs['placeholder'] = 'Create a strong password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    PrependedText('email', mark_safe("<i class='bi bi-envelope'></i>")), 
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    PrependedText('phone_number', mark_safe("<i class='bi bi-phone'></i>")), 
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row mb-2'
            ),
            
            Row(
                Column(
                    PrependedText('nin', "NIN"), 
                    css_class='form-group col-md-6 mb-0'
                ),
                Column(
                    PrependedText('bvn', "BVN"), 
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
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