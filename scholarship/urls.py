from django.urls import path
from . import views, application_views as app_views

app_name = 'scholarship'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_scholarship, name='create'),
    path('<int:id>/', views.scholarship, name='scholarship'),
    path('<int:id>/field-of-studies/', views.field_of_studies, name='field_of_studies'),
    path('<int:id>/update/', views.update_scholarship, name='update'),
    path('<int:id>/delete/', views.delete_scholarship, name='delete'),
    
    # Registration Documents
    path('app-documents/<int:id>/', views.app_docuements, name='app-documents'),
    path('app-documents/<int:id>/create/', views.create_app_docuement, name='create-app-document'),
    path('app-documents/<int:id>/update/', views.update_app_document, name='update-app-document'),
    path('app-documents/<int:id>/delete/', views.delete_app_document, name='delete-app-document'),

    path('applications/', app_views.applications, name='applications'),
    path('applications/<int:id>', app_views.scholarship_applications, name='scholarship-applications'),
    path('applications/<str:application_id>', app_views.application, name='application'),
    path('applications/<int:id>/approve', app_views.approve_application, name='approve-application'),
    path('applications/<int:id>/reject', app_views.reject_application, name='reject-application'),

    path('disbursements/<int:id>', app_views.scholarship_disbursements, name='scholarship-disbursement'),

]
