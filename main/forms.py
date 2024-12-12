from django import forms
from .models import FAQ, Article, Contact, Notification


class FAQForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['placeholder'] = 'Enter frequently asked question'
        self.fields['answer'].widget.attrs['placeholder'] = 'Answer frequently asked question'

    class Meta:
        model = FAQ
        fields = ("question", "answer")


class ArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['headline'].widget.attrs['placeholder'] = 'Enter article headline'
        self.fields['content'].widget.attrs['placeholder'] = 'Enter article content'
        
    class Meta:
        model = Article
        fields = ('headline', 'headline_image', 'content', 'is_public')

class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].widget.attrs['placeholder'] = 'Enter message subject'
        self.fields['message'].widget.attrs['placeholder'] = 'Enter your message'
    
    class Meta:
        model = Contact
        fields = ("subject", "message", )

class NotificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs['placeholder'] = 'Enter notification message'

    class Meta:
        model = Notification
        fields = ("message", 'visibility')
