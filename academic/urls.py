from django.urls import path
from . import views

app_name = 'academic'

urlpatterns = [
    # Institution Types
    path('institution-types/', views.institution_types, name='institution-types'),
    path('institution-type/', views.institution_type, name='institution-type'),
    path('institution-types/create/', views.create_institution_type, name='create-institution-type'),
    path('institution-types/<int:id>/update/', views.update_institution_type, name='update-institution-type'),
    path('institution-types/<int:id>/delete/', views.delete_institution_type, name='delete-institution-type'),
    
    # Institutions
    path('institutions/', views.institutions, name='institutions'),
    path('institutions/create/', views.create_institution, name='create-institution'),
    path('institutions/<int:id>/update/', views.update_institution, name='update-institution'),
    path('institutions/<int:id>/delete/', views.delete_institution, name='delete-institution'),
    
    # Programs 
    path('programs/', views.programs, name='programs'),
    path('program/', views.program, name='program'),
    path('programs/create/', views.create_program, name='create-program'),
    path('programs/<int:id>/update/', views.update_program, name='update-program'),
    path('programs/<int:id>/delete/', views.delete_program, name='delete-program'),
    
    # Field of studies
    path('field-of-studies/', views.field_of_studies, name='field-of-studies'),
    path('field-of-study/', views.field_of_study, name='field-of-study'),
    path('field-of-studies/create/', views.create_field_of_study, name='create-field-of-study'),
    path('field-of-studies/<int:id>/update/', views.update_field_of_study, name='update-field-of-study'),
    path('field-of-studies/<int:id>/delete/', views.delete_field_of_study, name='delete-field-of-study'),
    
    # Courses
    path('courses/', views.courses, name='courses'),
    path('courses/create/', views.create_course, name='create-course'),
    path('courses/<int:id>/update/', views.update_course, name='update-course'),
    path('courses/<int:id>/delete/', views.delete_course, name='delete-course'),
    
    # Levels
    path('levels/', views.levels, name='levels'),
    path('levels/create/', views.create_level, name='create-level'),
    path('levels/<int:id>/update/', views.update_level, name='update-level'),
    path('levels/<int:id>/delete/', views.delete_level, name='delete-level'),
]
