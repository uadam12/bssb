from django.urls import reverse
from django.shortcuts import get_object_or_404
from app.auth import officials_only
from app.views import data_view, update_view, create_view, delete_view
from .forms import SubjectForm, GradeForm
from .models import Subject, Grade


@officials_only()
def index(request):
    pass

# Subjects
@officials_only()
def subjects(request):
    return data_view(
        request=request, 
        data=Subject.objects.all(),
        add_url=reverse('ssce:create-subject'),
        data_template='ssce/subjects.html', title='SSCE Subjects',
        table_headers=['S/N', "Name", 'Is Compulsory', 'Actions']
    )

@officials_only(main_admin_only=True)
def create_subject(request):
    return create_view(request, 
        form_header='Create Subject',
        form_class=SubjectForm, success_url='ssce:subjects', 
    )

@officials_only(main_admin_only=True)
def update_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    
    return update_view(
        request, instance=subject, form_class=SubjectForm, 
        form_header='Update Subject'
    )
    
@officials_only(main_admin_only=True)
def delete_subject(request, id):
    subject = get_object_or_404(Subject, id=id)
    return delete_view(request, model=subject, header='Delete Subject')

# Grades
@officials_only()
def grades(request):
    return data_view(
        request=request, 
        data=Grade.objects.all(),
        add_url=reverse('ssce:create-grade'),
        data_template='ssce/grades.html', title='SSCE Grades',
        table_headers=['S/N', "Name", 'Value', 'Actions']
    )

@officials_only(main_admin_only=True)
def create_grade(request):
    return create_view(request, 
        form_header='Create Grade',
        form_class=GradeForm, success_url='ssce:grades', 
    )

@officials_only(main_admin_only=True)
def update_grade(request, id):
    grade = get_object_or_404(Grade, id=id)
    
    return update_view(
        request, instance=grade, form_class=GradeForm, 
        form_header='Update Grade'
    )
    
@officials_only(main_admin_only=True)
def delete_grade(request, id):
    grade = get_object_or_404(Grade, id=id)
    return delete_view(request, model=grade, header='Delete Grade')