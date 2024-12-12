from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate
from app import render, is_post
from app.auth import login_required, redirect, messages, logout_required
from users.models import User
from .forms import LoginForm, RegisterForm


# Create your views here.
@login_required
def toggle_2fa(request:HttpRequest):
    user:User = request.user
    
    if not user.otp:
        user.generate_otp
    
    if is_post(request):
        otp = request.POST.get('otp', '')
        user_otp = user.get_otp
        
        if user_otp and user_otp.verify(otp):
            user.otp_enabled = True
            user.save()
            messages.success(request, 'Two Factor Authentication enabled successfully.')
            return redirect(user.profile)
        else: messages.error(request, 'Failed to activate Two Factor Authentication.')
    
    return render(request, 'auth/activate-otp', 'Activate Two Factor Authentication')

@logout_required
def login_user(request:HttpRequest):
    form = LoginForm()
    
    if is_post(request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.data.get('email')
            password = form.data.get('password')
            user:User = authenticate(request, email=email, password=password)
            
            if user is None:
                messages.error(request, "Invalid password and/or email address." )
            elif user.otp_enabled or user.access_code > 2:
                request.session['otp_user_id'] = user.id
                return redirect('auth:verify-login-otp')
            else:
                login_user(request, user)
                messages.success(request, 'You have login successfully!!!')
                return redirect(user.dashboard)

    return render(request, 'auth/login', title = 'Welcome back to BSSB', form=form)

def verify_login_otp(request:HttpRequest):
    user_id = request.session.get('otp_user_id', None)
    
    if not user_id:
        return redirect('auth:login')
    
    user = get_object_or_404(User, id=user_id)
    user_otp = user.get_otp