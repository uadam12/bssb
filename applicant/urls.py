from django.urls import path
from . import views

app_name = 'applicant'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile-info/', views.profile, name='profile'),
    path('personal-info/', views.personal_information, name='save-personal-info'),
    path('academic-info/', views.academic_information, name='save-academic-info'),
    path('bank-info/', views.account_details, name='save-bank-info'),
    path('documents/', views.documents, name='save-document'),
    path('referees/', views.referees, name='save-referee'),
    path('scholarships/', views.scholarships, name='scholarships'),
    path('apply/<int:id>/', views.apply, name='apply'),
    
    path('schools-attended/', views.schools_attended, name='schools-attended'),
    path('schools-attended/add/', views.add_school, name='add-school'),
    path('schools-attended/<int:pk>/update/', views.update_school, name='update-school'),
    path('schools-attended/<int:pk>/delete/', views.delete_school, name='delete-school'),
    path('change-profile-picture', views.change_profile_picture, name='change-profile-picture')
]
