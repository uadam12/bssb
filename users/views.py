from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as login_user, logout as logout_user, authenticate
from app import render, is_post
from app.views import update_view
from app.token import verify_token
from app.auth import login_required, logout_required, blocked_required
from board.models import Board
from .forms import RegisterForm, LoginForm, EmailForm, UserForm, ProfilePictureForm, ResetPasswordForm
from .emails import send_activation_email, send_recovery_email

# Create your views here.
@login_required
def change_picture(request):
    return update_view(
        request,
        instance=request.user,
        form_class=ProfilePictureForm,
        success_url='applicant:profile',
        template='users/change-picture'
    )

@login_required
def update_name(request):
    return update_view(
        request,
        instance=request.user,
        success_url='applicant:profile',
        form_class=UserForm,
        header='Update name',
        template='users/update-name'
    )

# Auth
@logout_required
def register(request):
    board = Board.load()
    
    if not board.registration_is_open:
        return render(request, 'users/registration-closed', "Registration closed")
    form = RegisterForm
    
    if is_post(request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            sent = send_activation_email(request, user)

            if sent:
                login_user(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('user:login')

    return render(request, 'users/register', title='Board Registration', with_htmx=True, form=form)

def activate(request, token):
    User = get_user_model()
    email = verify_token(token)
    user = User.objects.filter(email=email)
    
    if user.exists():
        user = user.first()
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for your email confirmation. Now you can complete your profile information.')
        return redirect('applicant:profile')
    
    messages.error(request, 'Activation link is invalid!')
    return redirect('user:inactive')


@login_required
def inactive(request):
    return render(request, 'users/inactive')

@logout_required
def login(request):
    form = LoginForm()
    
    if is_post(request):
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.data.get('email')
            password = form.data.get('password')
            user = authenticate(request, email=email, password=password)
            
            if user is None:
                messages.error(request, "Invalid password and/or email address." )
            else:
                login_user(request, user)
                messages.success(request, 'You have login successfully!!!')
                return redirect(user.dashboard)
        else: messages.error(request, str(form.error_messages))

    return render(request, 'users/login', title = 'Board Login', form=form)

@login_required
def logout(request):
    if is_post(request):
        messages.success(request, 'You have logout successfully!')
        logout_user(request)
    
    return redirect('user:login')

@logout_required
def forgot_password(request):
    form = EmailForm()
    
    if is_post(request):
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = get_user_model().objects.filter(email=email)

            if user.exists():
                user = user.first()
                
                sent = send_recovery_email(request, user)
                if sent:
                    messages.success(request, 'Account recovery instruction(s) sent successfully.')
            
    return render(request, 'users/forgot-password', title='BSSB Forgot password', form=form)

@logout_required
def reset_password(request, token):
    email = verify_token(token)
    
    if not email:
        return redirect('user:login')

    user = get_user_model().objects.filter(email=email)
    if not user.exists():
        messages.error(request, 'No account is associated with this email address')
        return redirect('user:login')

    form = ResetPasswordForm()
    
    if is_post(request):
        form = ResetPasswordForm(request.POST)
        
        if form.is_valid():
            password = form.cleaned_data['password']
            user = user.first()
            user.set_password(password)
            user.save()
            messages.success(request, 'Password updated successfully. Try your new password.')
            return redirect('user:login')


    return render(request, 'users/reset-password', 'BSSB | Reset Password', form=form)

@blocked_required    
def block(request):
    return render(request, 'users/block', 'BSSB | Block account')