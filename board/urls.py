from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.update, name='update'),
    
    # Registration Documents
    path('reg-documents/', views.reg_docuements, name='reg-documents'),
    path('reg-documents/create/', views.create_reg_docuement, name='create-reg-document'),
    path('reg-documents/<int:id>/update/', views.update_reg_document, name='update-reg-document'),
    path('reg-documents/<int:id>/delete/', views.delete_reg_document, name='delete-reg-document'),
    
    # Banks
    path('banks/', views.banks, name='banks'),
    path('accounts/', views.accounts, name='accounts'),
    path('banks/create/', views.create_bank, name='create-bank'),
    path('banks/<str:code>/update/', views.update_bank, name='update-bank'),
    path('banks/<str:code>/delete/', views.delete_bank, name='delete-bank'),
    
    # Local Government Area(LGA)
    path('lgas/', views.lgas, name='lgas'),
    path('lgas/create/', views.create_lga, name='create-lga'),
    path('lgas/<str:code>/update/', views.update_lga, name='update-lga'),
    path('lgas/<str:code>/delete/', views.delete_lga, name='delete-lga'),
]
