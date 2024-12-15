from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib import messages
from django.core.validators import EmailValidator
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from crispy_forms.templatetags.crispy_forms_filters import as_crispy_field
from app import render, is_post
from app.token import verify_token
from app.auth import logout_required, login_required, blocked_required, inactive_required
from board.models import Board
from users.models import User
from .forms import RegisterForm, LoginForm
from .emails import send_activation_email, send_login_verification_link, send_recovery_email


def validate_field(request, field):
    form = RegisterForm(request.POST)
    form.is_valid()
    return HttpResponse(as_crispy_field(form[field]))

def nin(request):
    return validate_field(request, 'nin')

def bvn(request):
    return validate_field(request, 'bvn')

def email(request):
    return validate_field(request, 'email')
 
def phone_number(request):
    return validate_field(request, 'phone_number')

@logout_required
def signup(request):
    if not Board.load().registration_is_open: return render(
        request, 'auth/registration-closed', "Registration closed"
    )

    if is_post(request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully!')

            if send_activation_email(request, user):
                messages.info(request, 'Account activation instructions is sent your email address.')

            return redirect('auth:signup-complete')
    else: form = RegisterForm()

    return render(request, 'auth/register', title='New Account Registration', with_htmx=True, form=form)

@logout_required
def signin(request):
    form = LoginForm()

    if is_post(request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user:User = authenticate(
                request, 
                email=form.cleaned_data.get('email'), 
                password=form.cleaned_data.get('password')
            )

            if user is None: 
                messages.error(request, "Invalid password and/or email address.")
            elif (user.otp_enabled or user.access_code > 2) and send_login_verification_link(request, user):
                messages.success(
                    request, 
                    "We have successfully sent signin verification instruction(s) to your email."
                )
                return redirect('main:home')
            elif user.access_code < 2 and not user.otp_enabled:
                login(request, user)
                messages.success(request, 'You have signin successfully!!!')
                return redirect(user.dashboard)

    return render(request, 'auth/login', title='Welcome Back', form=form)

@logout_required
def signup_complete(request):
    if is_post(request):
        try:
            email = request.POST.get('email').strip()
            EmailValidator()(email)
            user = User.objects.filter(email=email).first()
            
            if user is None:
                messages.error(request, 'Failed to fetch your account details.')
            elif user.is_active:
                messages.error(request, 'Your account is already activated. Please sign in')
                return redirect('auth:signin')
        except:
            messages.error(request, "Invalid Email address")

    return render(request, 'auth/register-complete', 'Registration Completed')


def activate(request, token):
    user = User.objects.filter(email=verify_token(token)).first()
    
    if user is not None:
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for your email confirmation.')
        messages.info(request, 'Please complete your profile information.')
        return redirect(user.profile)
    
    messages.error(request, 'Accont activation link is invalid/expired!')
    return redirect('auth:inactive')

@logout_required
def signin_verification(request, token):
    user = User.objects.filter(email=verify_token(token)).first()

    if user is not None:
        login(request, user)
        messages.success(request, 'You have sign in successfully!!!')
        return redirect(user.dashboard)
    
    messages.error(request, 'Signin verification link is invalid/expired!')
    return redirect('auth:signin')


@inactive_required
def inactive(request):
    return render(request, 'auth/inactive')

@login_required
def signout(request):
    if is_post(request):
        messages.success(request, 'You have logout successfully!')
        logout(request)

    return redirect('auth:signin')

@login_required
def change_password(request):
    if is_post(request):
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            user:User = form.save()
            logout(request)
            login(request, user)
            messages.success(request, 'Password updated successfully.')
            return redirect(user.profile)

    else: form = PasswordChangeForm(request.user)

    return render(request, 'auth/change-password', 'Change Your Password', form=form)

@logout_required
def forgot_password(request):
    if is_post(request):
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data.get('email')).first()

            if user is not None and send_recovery_email(request, user):
                messages.success(request, 'Account recovery instruction(s) sent successfully.')    
                return redirect('main:home')
            
            messages.info(
                request, 'Failed to send recovery instructions. '+
                'Please check, if you type your email address correctly.'
            )
    else: form = PasswordResetForm()

    return render(request, 'auth/forgot-password', title='Recover Forgot password', form=form)

@logout_required
def reset_password(request, token):
    email = verify_token(token)

    if not email:
        messages.error(request, "Account recover link is invalid/expired.")
        return redirect('auth:signin')

    user = User.objects.filter(email=email).first()
    if user is None:
        messages.error(request, f"Account does not exists with this email address({email}).")
        return redirect('auth:signin')

    if is_post(request):
        form = SetPasswordForm(user=user, data=request.POST)
        if form.is_valid() and form.save():
            messages.success(request, 'Account recovered successfully.')
            messages.info(request, 'Please signin with your new password.')
            return redirect('auth:signin')
    else: form = SetPasswordForm(user=user)

    return render(request, 'auth/reset-password', 'Reset Your Password', form=form)

@blocked_required
def block(request):
    return render(request, 'auth/block', 'Account Blocked')