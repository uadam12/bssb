import django_filters as df
from django import forms
from django.db.models import Q
from crispy_forms.layout import Layout
from app.filter import FilterDataSet
from .models import FAQ, Article, Contact, Notification


class FAQFilter(FilterDataSet):
    term = df.CharFilter(method='filter_faq')
    
    class Meta:
        model = FAQ
        fields = ('question', )

    def filter_faq(self, queryset, _, value):
        return queryset.filter(
            Q(question__icontains=value) | 
            Q(answer__icontains=value)
        )
    
    @property
    def form(self):
        form = super().form
        
        form.fields['term'].label = ''
        form.fields['term'].widget.attrs['placeholder'] = 'Search FAQs'
        form.helper.layout = Layout(
            self.search_field_with_btn('term')
        )
        
        return form
    
class NotificationFilter(FilterDataSet):
    message = df.CharFilter(
        label='', field_name='message', lookup_expr='icontains',
        widget = forms.TextInput(attrs={
            'placeholder': 'Search official'
        })
    )
    visibility = df.ChoiceFilter(
        widget=forms.RadioSelect(), empty_label='All Notifications', 
        field_name='visibility', choices = Notification.VISIBILITIES
    )
    
    class Meta:
        model = Notification
        fields = []
    
    @property
    def form(self):
        form = super().form
        
        form.fields['message'].label = ''
        form.fields['message'].widget.attrs['placeholder'] = 'Search notification'
        form.helper.layout = Layout(
            'visibility',
            self.search_field_with_btn('message')
        )
        
        return form
    
class ContactFilter(FilterDataSet):
    message = df.CharFilter(
        label='', method='filter_contact',
        widget = forms.TextInput(attrs={
            'placeholder': 'Search official'
        })
    )
    
    def filter_contact(self, queryset, _, value):
        return queryset.filter(
            Q(subject__icontains=value) | 
            Q(message__icontains=value)
        )

    class Meta:
        model = Contact
        fields = ('message', )

    @property
    def form(self):
        form = super().form
        
        form.fields['message'].label = ''
        form.fields['message'].widget.attrs['placeholder'] = 'Search notification'
        form.helper.layout = Layout(
            self.search_field_with_btn('message')
        )
        
        return form

class ArticleFilter(FilterDataSet):
    term = df.CharFilter(method='filter_article')
    publish_from = df.DateFilter(
        field_name='publish_on', lookup_expr='gte',
        label='Publish from', widget = forms.DateInput(attrs={
            'type': 'date'
        })
    )
    publish_to = df.DateFilter(
        field_name='publish_on', lookup_expr='lte',
        label='Publish before', widget = forms.DateInput(attrs={
            'type': 'date'
        })
    )
    
    class Meta:
        model = Article
        fields = ('headline', )

    def filter_article(self, queryset, _, value):
        return queryset.filter(
            Q(headline__icontains=value) | 
            Q(content__icontains=value)
        )
    
    @property
    def form(self):
        form = super().form
        
        form.fields['term'].label = ''
        form.fields['term'].widget.attrs['placeholder'] = 'Search Article/News'
        form.helper.layout = Layout(
            'publish_from', 'publish_to',
            self.search_field_with_btn('term')
        )
        
        return form