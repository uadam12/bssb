from django import forms
import django_filters as df
from crispy_forms.layout import Layout
from app.filter import FilterDataSet
from .models import Ticket, Message

class TicketFilter(FilterDataSet):
    name = df.CharFilter(
        'name', lookup_expr='icontains', 
        label='', widget = forms.TextInput(attrs={
            'placeholder': 'Search ticket'
        })
    )
    
    is_resolved = df.ChoiceFilter(
        'is_resolved', label='', empty_label='Both',
        choices=((True, 'Resolved'), (False, 'Open')), 
        widget=forms.RadioSelect()
    )
    
    date_from = df.DateFilter(
        label='From range',
        field_name='created_on', lookup_expr='gte',
        widget=forms.DateInput({'type': 'date'})
    )
    
    date_to = df.DateFilter(
        label='To range',
        field_name='created_on', lookup_expr='lte',
        widget=forms.DateInput({'type': 'date'})
    )
    
    class Meta:
        model = Ticket
        fields = ['is_resolved']
        
    @property
    def form(self):
        form = super().form
        form.helper.layout = Layout(
            'date_from', 'date_to', 'is_resolved',
            self.search_field_with_btn('name')
        )
        
        return form
        

class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['placeholder'] = 'Enter ticket name'

    class Meta:
        model = Ticket
        fields = ("name", )

class MessageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['content'].label = ''
        self.fields['content'].widget.attrs['placeholder'] = 'Enter your message/complain'
    
    class Meta:
        model = Message
        fields = ("content", )
