from django.urls import path
from . import views

app_name = 'ssce'

urlpatterns = [
    path('', views.index, name='index'),

    # Subject
    path('subjects/', views.subjects, name='subjects'),
    path('subjects/create/', views.create_subject, name='create-subject'),
    path('subjects/<str:code>/update/', views.update_subject, name='update-subject'),
    path('subjects/<str:code>/delete/', views.delete_subject, name='delete-subject'),
    
    # Grade
    path('grades/', views.grades, name='grades'),
    path('grades/create/', views.create_grade, name='create-grade'),
    path('grades/<str:code>/update/', views.update_grade, name='update-grade'),
    path('grades/<str:code>/delete/', views.delete_grade, name='delete-grade'),
]
