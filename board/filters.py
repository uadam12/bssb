from django import forms
from django.db.models import Q
import django_filters as df
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import InlineRadios
from app.filter import FilterDataSet
from .models import Bank, LGA


class BankFilter(FilterDataSet):
    name = df.CharFilter(field_name='name', method='filter_bank')
    is_available = df.ChoiceFilter(
        empty_label = 'Both',
        widget = forms.RadioSelect(),
        field_name='is_available', label='',
        choices = [(True, 'Available'), (False, 'unavailable')]
    )
    
    class Meta:
        model = Bank
        fields = ('name', 'is_available')
    
    def filter_bank(self, queryset, _, value):
        return queryset.filter(Q(name__icontains=value) | Q(code__icontains=value))

    @property
    def form(self):
        form = super().form
        
        form.fields['name'].widget.attrs['placeholder'] = 'Search Bank'
        form.fields['name'].label = ''
        form.helper.layout = Layout(
            InlineRadios('is_available'),
            self.search_field_with_btn('name')
        )
        
        return form

class LGAFilter(FilterDataSet):
    name = df.CharFilter(field_name='name', method='filter_lga')
    class Meta:
        model = LGA
        fields = ('name', )

    def filter_lga(self, queryset, _, value):
        return queryset.filter(Q(name__icontains=value) | Q(code__icontains=value))
    
    @property
    def form(self):
        form = super().form
        
        form.fields['name'].label = ''
        form.fields['name'].widget.attrs['placeholder'] = 'Search Local Government Area'
        form.helper.layout = Layout(self.search_field_with_btn('name'))
        
        return form