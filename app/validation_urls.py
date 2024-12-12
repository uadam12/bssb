from django.urls import path
import app.validation_views as views

app_name = 'validate'

urlpatterns = [
    path('nin/', views.nin, name='nin'),
    path('bvn/', views.bvn, name='bvn'),
    path('email/', views.email, name='email'),
    path('phone_number/', views.phone_number, name='phone_number'),
]