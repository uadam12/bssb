from django import forms
from .models import SSCE, Subject, Grade, Record

class SSCEForm(forms.ModelForm):
    
    class Meta:
        model = SSCE
        fields = ("school", "serial_number", "graduation_year", "exam_number", "ssce_type")

class SubjectForm(forms.ModelForm):
    
    class Meta:
        model = Subject
        fields = ("name", "is_compulsory")

class GradeForm(forms.ModelForm):
    
    class Meta:
        model = Grade
        fields = ("name", "value")

class RecordForm(forms.ModelForm):
    
    class Meta:
        model = Record
        fields = ("subject", "grade")
