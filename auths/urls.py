from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('signin/', views.signin, name='signin'), path('signup/', views.signup, name='signup'),
    path('signup-complete/', views.signup_complete, name='signup-complete'),
    path('nin/', views.nin, name='nin'), path('bvn/', views.bvn, name='bvn'),
    path('email/', views.email, name='email'),
    path('activate/<token>', views.activate, name='activate'),
    path('signin/<token>', views.signin_verification, name='signin-verification'),
    path('phone_number/', views.phone_number, name='phone_number'),
    path('reset/<token>', views.reset_password, name='reset-password'),
    path('inactive/', views.inactive, name='inactive'),
    path('change-password/', views.change_password, name='change-password'),
    path('forgot-password/', views.forgot_password, name='forgot-password'),
    path('logout/', views.signout, name='signout'),
    path('account-blocked/', views.block, name='block'),
]
