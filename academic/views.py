from django.shortcuts import get_object_or_404
from django.urls import reverse
from app import render
from app.views import update_view, delete_view, create_view, data_view
from app.auth import officials_only
from .filters import (
    CourseFilter, LevelFilter, InstitutionFilter, 
    FieldOfStudyFilter, ProgramFilter, InstitutionTypeFilter
)
from .forms import (
    InstitutionType, InstitutionTypeForm,
    FieldOfStudy, FieldOfStudyForm,
    Institution, InstitutionForm,
    Program, ProgramForm,
    Course, CourseForm,
    Level, LevelForm
)


# Institution Types
@officials_only()
def institution_types(request):
    filter = InstitutionTypeFilter(request.GET, queryset=InstitutionType.objects.all())
    return data_view(
        request, title='Institution Types',
        data_template="academic/institution-types.html",
        table_headers=['S/N', 'Name', 'Action'], filter_form=filter.form,
        data=filter.qs, add_url=reverse('academic:create-institution-type')
    )

def institution_type(request):
    id = request.GET.get('institution_type')
    return render(
        request, 'parts/options', 
        data=Institution.objects.filter(institution_type=id), 
        empty_label=f'Select your institution'
    )

@officials_only(admin_only=True)
def create_institution_type(request):
    return create_view(
        request, form_class=InstitutionTypeForm, 
        success_url='academic:institution-types', 
        form_header='Create Institution Type'
    )

@officials_only(admin_only=True)
def update_institution_type(request, id):
    inst_type = get_object_or_404(InstitutionType, id=id)
    
    return update_view(
        request, instance=inst_type, 
        form_class=InstitutionTypeForm, 
        form_header=f'Update {inst_type}'
    )

@officials_only(admin_only=True)
def delete_institution_type(request, id):
    inst_type = get_object_or_404(InstitutionType, id=id)
    return delete_view(request, model=inst_type, header='Delete Institution Type')

# Institutions
@officials_only()
def institutions(request):
    filter = InstitutionFilter(request.GET, queryset=Institution.objects.all())
    return data_view(
        request, title='Institutions',
        data_template="academic/institutions.html",
        table_headers=['S/N', 'Name', 'Type', 'Action'], filter_form=filter.form,
        data=filter.qs.prefetch_related('institution_type'), add_url=reverse('academic:create-institution')
    )

@officials_only(admin_only=True)
def create_institution(request):
    return create_view(
        request, form_class=InstitutionForm, 
        success_url='academic:institutions', 
        form_header='Create Institution'
    )

@officials_only(admin_only=True)
def update_institution(request, id):
    institution = Institution.objects.get(id=id)

    return update_view(
        request, 
        instance=institution, 
        form_class=InstitutionForm, 
        form_header='Update Institution'
    )
    
@officials_only(admin_only=True)
def delete_institution(request, id):
    institution = Institution.objects.get(id=id)
    
    return delete_view(
        request, model=institution,
        header='Delete Institution'
    )


# Programs
@officials_only()
def programs(request):
    filter = ProgramFilter(request.GET, queryset=Program.objects.all())

    return data_view(request, 
        data_template="academic/programs.html",
        title='Programs', filter_form=filter.form,
        table_headers=['S/N', 'Program Name', 'Action'],
        data=filter.qs, add_url=reverse('academic:create-program')
    )

def program(request):
    id = request.GET.get('program')

    return render(
        request, 'parts/field-of-study', 
        levels=Level.objects.filter(program=id), 
        field_of_studies=FieldOfStudy.objects.filter(program=id)
    )

@officials_only(admin_only=True)
def create_program(request):
    return create_view(
        request, form_class=ProgramForm, 
        success_url='academic:programs',
        form_header='Create Program'
    )

@officials_only(admin_only=True)
def update_program(request, id):
    program = get_object_or_404(Program, id=id)
    
    return update_view(
        request, instance=program, 
        form_class=ProgramForm, form_header='Update Program'
    )

@officials_only(admin_only=True)    
def delete_program(request, id):
    program = get_object_or_404(Program, id=id)
    return delete_view(request, model=program, header='Delete Program')


# Field of studies
@officials_only()
def field_of_studies(request):
    filter = FieldOfStudyFilter(request.GET, queryset=FieldOfStudy.objects.all())

    return data_view(request, 
        data_template="academic/field-of-studies.html",
        title='Field of studies', filter_form=filter.form,
        table_headers=['S/N', 'Name', 'Program', 'Action'],
        data=filter.qs.prefetch_related('program'), 
        add_url=reverse('academic:create-field-of-study')
    )

def field_of_study(request):
    id = request.GET.get('field_of_study')

    return render(
        request, 'parts/options', empty_label=f'Select your course of study',
        data=Course.objects.filter(field_of_study=id)
    )

@officials_only(admin_only=True)
def create_field_of_study(request):
    return create_view(
        request, form_class=FieldOfStudyForm, 
        success_url=FieldOfStudy.list_url,
        form_header='Create field of study'
    )

@officials_only(admin_only=True)
def update_field_of_study(request, id):
    field_of_study = get_object_or_404(FieldOfStudy, id=id)
    
    return update_view(
        request, instance=field_of_study, 
        form_class=FieldOfStudyForm, 
        form_header='Update field of study'
    )

@officials_only(admin_only=True)
def delete_field_of_study(request, id):
    field_of_study = get_object_or_404(FieldOfStudy, id=id)
    return delete_view(request, model=field_of_study, header='Delete field of study')

# Courses
@officials_only()
def courses(request):
    filter = CourseFilter(request.GET, queryset=Course.objects.all())
    return data_view(
        request, title='Courses',
        filter_form = filter.form,
        data_template="academic/courses.html",
        add_url=reverse('academic:create-course'),
        data=filter.qs.prefetch_related('field_of_study'), 
        table_headers=['S/N', 'Title', 'Field of Study', 'Action']
    )

@officials_only(admin_only=True)
def create_course(request):
    return create_view(
        request, form_class=CourseForm, 
        success_url='academic:courses', 
        form_header='Create Course'
    )

@officials_only(admin_only=True)
def update_course(request, id):
    course = get_object_or_404(Course, id=id)
    
    return update_view(request, instance=course, form_class=CourseForm, form_header='Update Course')

@officials_only(admin_only=True)
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    
    return delete_view(request, model=course, header='Delete Course')
    
# Levels
@officials_only()
def levels(request):
    filter = LevelFilter(request.GET, queryset=Level.objects.all())
    return data_view(
        request, filter_form = filter.form,
        title='Levels', data_template="academic/levels.html",
        table_headers=['S/N', 'Name', 'Code', 'Program', 'Action'],
        data=filter.qs.prefetch_related('program'), add_url=reverse('academic:create-level')
    )

@officials_only(admin_only=True)
def create_level(request):
    return create_view(
        request, form_class=LevelForm, 
        success_url='academic:levels', 
        form_header='Create Level'
    )

@officials_only(admin_only=True)
def update_level(request, id):
    level = get_object_or_404(Level, id=id)
    
    return update_view(
        request, instance=level, 
        form_class=LevelForm, 
        form_header='Update Level'
    )

@officials_only(admin_only=True)
def delete_level(request, id):
    level = get_object_or_404(Level, id=id)
    return delete_view(request, model=level, header='Delete Level')