import django_filters as df
from django import forms
from django.db.models import Q
from crispy_forms.layout import Layout
from app.filter import FilterDataSet
from academic.models import Institution, Program
from .models import Application, Scholarship


class FilterScholarship(FilterDataSet):
    class Meta:
        model = Scholarship
        fields = []

    title = df.CharFilter(
        field_name='title', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search by Name'
        })
    )

    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(self.search_field_with_btn('title'))
        return form


class ApplicationFilter(FilterDataSet):
    class Mete:
        model = Application
        fields = []
    
    term = df.CharFilter(
        label='', method='filter_application'
    )

    institution = df.ModelChoiceFilter(
        field_name = 'institution',
        label = 'Academic Institution',
        empty_label = 'Select Academic Institution',
        queryset = Institution.objects.all()
    )
    
    program = df.ModelChoiceFilter(
        field_name = 'program',
        empty_label = 'Select Program',
        label = 'Program',
        queryset = Program.objects.all()
    )
    
    status = df.ChoiceFilter(
        field_name = 'status',
        label = 'Application Status',
        empty_label = 'Select Application Status',
        choices = Application.STATUS
    )
    
    def filter_application(self, queryset, _, value):
        return queryset.filter(Q(application_id__icontains=value))

    @property
    def form(self):
        form = super().form
        form.fields['term'].widget.attrs['placeholder'] = 'Search applications'
        form.helper.layout = Layout(
            'status',  'program',
            self.search_field_with_btn('term')
        )
        
        return form