from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('change-profile-picture/', views.change_picture, name='change-picture'),
    path('change-name/', views.update_name, name='update-name'),
]
