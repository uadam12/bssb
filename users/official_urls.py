from django.urls import path
from . import official_views as views

app_name = 'official'

urlpatterns = [
    path('', views.officials, name='index'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_official, name='create'),
    path('<int:id>/delete', views.delete_official, name='delete'),
    path('<int:id>/update', views.update_official, name='update'),

    path('applicants/', views.applicants, name='applicants'),
    path('applicants/<int:applicant_id>/block', views.block_applicant, name='block-applicant'),
    path('applicants/<int:applicant_id>/unblock', views.unblock_applicant, name='unblock-applicant'),
    
]