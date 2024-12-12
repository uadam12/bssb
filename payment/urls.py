from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('', views.index, name='index'),
    path('registration-fee/', views.registration_fee, name='registration-fee'),
    path('registration-fee/verify', views.verify_reg_fee_payment, name='verify-reg-fee-payment'),
    path('application-fee/<int:id>', views.application_fee, name='application-fee'),
    path('application-fee/<int:id>/verify', views.verify_application_fee, name='verify-app-fee-payment'),
]
