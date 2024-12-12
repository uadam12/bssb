from django.http import HttpResponse
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from users.forms import RegisterForm

def validate_field(form, field):
    form.is_valid()
    return HttpResponse(as_crispy_field(form[field]))

def nin(request):
    return validate_field(RegisterForm(request.POST), 'nin')

def bvn(request):
    return validate_field(RegisterForm(request.POST), 'bvn')

def email(request):
    return validate_field(RegisterForm(request.POST), 'email')
 
def phone_number(request):
    return validate_field(RegisterForm(request.POST), 'phone_number')
