import django_filters as df
from django import forms
from crispy_forms.layout import Layout
from app.filter import FilterDataSet
from .models import Course, FieldOfStudy, Program, Level, Institution, InstitutionType


class SearchFilter(FilterDataSet):
    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search by Name'
        })
    )

    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(self.search_field_with_btn('name'))
        return form

class InstitutionTypeFilter(SearchFilter):
    class Mete:
        model = InstitutionType
        fields = ['name']


class ProgramFilter(SearchFilter):
    class Mete:
        model = Program
        fields = ['name']


class InstitutionFilter(FilterDataSet):
    class Mete:
        model = Institution
        fields = ('institution_type', 'name')

    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search institution'
        })
    )
    institution_type = df.ModelMultipleChoiceFilter(
        field_name = 'institution_type',
        queryset = InstitutionType.objects.all(),
        label = '', widget = forms.CheckboxSelectMultiple(attrs={
            'placeholder': 'Select institution type'
        })
    )
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'institution_type', 
            self.search_field_with_btn('name')
        )
        
        return form
    
class FieldOfStudyFilter(FilterDataSet):
    class Mete:
        model = FieldOfStudy
        fields = ('program', 'name', 'number_of_years')

    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search field of study'
        })
    )
    programs = df.ModelMultipleChoiceFilter(
        field_name = 'program',
        queryset = Program.objects.all(),
        label = '', widget = forms.CheckboxSelectMultiple(attrs={
            'placeholder': 'Select program'
        })
    )
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'programs', 'number_of_years',
            self.search_field_with_btn('name')
        )
        
        return form
    
class LevelFilter(FilterDataSet):
    class Mete:
        model = Level
        fields = ['name']
    
    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search Level by name'
        })
    )

    program = df.ModelMultipleChoiceFilter(
        field_name = 'program',
        queryset = Program.objects.all(),
        label = '', widget = forms.CheckboxSelectMultiple()
    )
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'program', 
            self.search_field_with_btn('name')
        )
        
        return form

class CourseFilter(SearchFilter):
    name = df.CharFilter(
        'title', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search by Name'
        })
    )
    
    field_of_study = df.ModelMultipleChoiceFilter(
        field_name = 'field_of_study',
        queryset = FieldOfStudy.objects.all(),
        label = '', widget = forms.CheckboxSelectMultiple()
    )

    class Mete:
        model = Course
        fields = []
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'field_of_study', self.search_field_with_btn('name')
        )
        
        return form