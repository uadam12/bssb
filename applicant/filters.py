import django_filters as df
from django.db.models import Q
from crispy_forms.layout import Layout
from app.filter import FilterDataSet
from .models import AccountBank


class AccountFilter(FilterDataSet):
    term = df.CharFilter(field_name='account_name', method='filter_account')
    class Meta:
        model = AccountBank
        fields = ('bank', )

    def filter_account(self, queryset, _, value):
        return queryset.filter(
            Q(account_name__icontains=value) | 
            Q(account_number__icontains=value)
        )
    
    @property
    def form(self):
        form = super().form
        
        form.fields['term'].label = ''
        form.fields['bank'].label = ''
        form.fields['bank'].empty_label = 'Select Bank'
        form.fields['term'].widget.attrs['placeholder'] = 'Search Account'
        form.helper.layout = Layout(
            'bank',
            self.search_field_with_btn('term')
        )
        
        return form

