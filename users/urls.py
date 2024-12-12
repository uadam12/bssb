from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('activate/<token>', views.activate, name='activate'),
    path('reset/<token>', views.reset_password, name='reset-password'),
    path('inactive/', views.inactive, name='inactive'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('logout/', views.logout, name='logout'),
    path('change-profile-picture/', views.change_picture, name='change-picture'),
    path('change-name/', views.update_name, name='update-name'),
    path('block/', views.block, name='block'),
]
