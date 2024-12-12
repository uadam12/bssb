import django_filters as df
from django import forms
from django.db.models import Q
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import InlineRadios
from app.filter import FilterDataSet
from board.models import LGA, Bank
from academic.models import Institution, Program, Course
from .models import User


class OfficalFilter(FilterDataSet):
    class Meta:
        model = User
        fields = []
    
    official_type = df.ChoiceFilter(
        field_name='access_code', method='filter_official_type',
        widget=forms.RadioSelect(), empty_label='Both', label='',
        choices = [('guest', 'Guest'), ('admin', 'Administrator')]
    )

    term = df.CharFilter(
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search official'
        }), method='filter_official'
    )
    
    def filter_official_type(self, queryset, _, value):
        if value:
            code = 3 if value == 'admin' else 2
            return queryset.filter(access_code=code)
        
        return queryset
        
    def filter_official(self, queryset, _, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(email__icontains=value)
        )

    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'official_type', self.search_field_with_btn('term')
        )
        return form

class ApplicantFilter(FilterDataSet):
    class Mete:
        model = User
        fields = []
    
    name = df.CharFilter(
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search applicants'
        }), method='filter_applicant'
    )

    lga = df.ModelChoiceFilter(
        field_name = 'personal_info__local_government_area',
        empty_label = 'Select Local Government Area',
        label = 'Local Government Area',
        queryset = LGA.objects.all(),
    )
    
    gender = df.ChoiceFilter(
        widget=forms.RadioSelect(),
        field_name='personal_info__gender',
        label = '', empty_label = 'Both',
        choices = (('Male', 'Male'), ('Female', 'Female'))
    )
    
    institution = df.ModelChoiceFilter(
        field_name = 'academic_info__institution',
        label = 'Academic Institution',
        empty_label = 'Select Academic Institution',
        queryset = Institution.objects.all(),
    )
    
    program = df.ModelChoiceFilter(
        field_name = 'academic_info__program',
        empty_label = 'Select Program',
        label = 'Program',
        queryset = Program.objects.all(),
    )
    
    course = df.ModelChoiceFilter(
        field_name = 'academic_info__course_of_study',
        empty_label = 'Select Course of Study',
        label = 'Academic Institution',
        queryset = Course.objects.all(),
    )
    
    bank = df.ModelChoiceFilter(
        field_name = 'account_bank__bank',
        empty_label = 'Select Bank',
        label = 'Account Bank',
        queryset = Bank.objects.all(),
    )
    
    def filter_applicant(self, queryset, _, value):
        return queryset.filter(
            Q(personal_info__phone_number__icontains=value) |
            Q(personal_info__bvn__icontains=value) |
            Q(personal_info__nin__icontains=value) |
            Q(first_name__icontains=value) | 
            Q(last_name__icontains=value) | 
            Q(email__icontains=value)
        )

    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'lga',  'bank', 'institution', 'program', 
            'course', InlineRadios('gender'),
            self.search_field_with_btn('name')
        )
        
        return form
    