import django_filters as df
from django import forms
from crispy_forms.layout import Layout
from app.filter import FilterDataSet
from .models import Payment

class PaymentFilter(FilterDataSet):
    rrr = df.CharFilter(
        field_name='rrr', lookup_expr='icontains', label='',
        widget=forms.TextInput({'placeholder': 'Search payment'})
    )
    
    date_from = df.DateFilter(
        label='From range',
        field_name='paid_on', lookup_expr='gte',
        widget=forms.DateInput({'type': 'date'})
    )
    
    date_to = df.DateFilter(
        label='To range',
        field_name='paid_on', lookup_expr='lte',
        widget=forms.DateInput({'type': 'date'})
    )

    class Mete:
        model = Payment
        fields = ('rrr', )

    payment_type = df.ChoiceFilter(
        field_name = 'payment_type',
        label = 'Payment Type',
        empty_label = 'Select Payment Type',
        choices = Payment.TYPES
    )
    
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'payment_type', 'date_from', 'date_to',
            self.search_field_with_btn('rrr')
        )
        
        return form