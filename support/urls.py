from django.urls import path
from . import views


app_name = 'support'
urlpatterns = [
    path('', views.index, name='index'),
    path('tickets/', views.tickets, name='tickets'),
    path('tickets/<int:id>/', views.ticket, name='ticket'),
    path('tickets/create/', views.create_ticket, name='create-ticket'),
    path('tickets/<int:id>/resolve/', views.ticket_resolve, name='ticket-resolve'),
]