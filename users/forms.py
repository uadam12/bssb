from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.layout import Layout, Row, Column, Div, Submit
from crispy_forms.helper import FormHelper

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('picture', )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            'picture',
            Div(
                Submit('save', 'Update Your Profile Picture'),
                css_class='text-end'
            )
        )

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your firstname'
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your lastname'
        self.fields['last_name'].widget.attrs['required'] = True
        
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            )
        )

class UserAddForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', )

class UserEditForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', )