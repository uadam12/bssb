from django import forms
from .models import Scholarship, ApplicationDocument


class ScholarshipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['title'].widget.attrs['placeholder'] = 'Enter Scholarship title'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter scholarship purpose, seperete paragraphs with new line'
        self.fields['eligibility_criteria'].widget.attrs['placeholder'] = 'Enter eligibility criteria, seperete paragraphs with new line'
        self.fields['application_fee'].widget.attrs['placeholder'] = 'Enter Scholarship Application FEE'
        self.fields['application_commence'].widget = forms.DateInput(attrs={
            'required': True, 'type': "date",
            'title': 'Select application commencement date'
        })
        self.fields['application_deadline'].widget = forms.DateInput(attrs={
            'required': True, 'type': "date",
            'title': 'Select application deadline date'
        })
        
        
    class Meta:
        model = Scholarship
        fields = (
            "title", "application_fee", 
            "application_commence", "application_deadline", 
            "description", "eligibility_criteria", "status"
        )


class ApplicationDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicationDocument
        fields = ("name", "required")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['placeholder'] = 'Enter application document name'

ApplicationDocumentForms = forms.modelformset_factory(
    ApplicationDocument, form=ApplicationDocumentForm, extra=0
)