from functools import wraps
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from . import is_htmx

def unauthorized_response(request, url):
    if is_htmx(request):
        return HttpResponse(status=403)

    return redirect(url)

def login_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            messages.info(request, 'You need to signin to access this page.')
            return unauthorized_response(request, 'auth:signin')
        
        if user.is_blocked:
            messages.error(request, 'Looks like your account is blocked.')
            return unauthorized_response(request, 'auth:block')

        if not user.is_active:
            messages.info(request, 'You need to activate your to access this page.')
            return unauthorized_response(request, 'auth:activation')
        
        return view(request, *args, **kwargs)
    return wrapper

def logout_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'You are already authenticated.')
            return unauthorized_response(request, request.user.dashboard)

        return view(request, *args, **kwargs)
    return wrapper

def inactive_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.is_active:
            messages.info(request, 'Your account is already activated.')
            return unauthorized_response(request, request.user.dashboard)
        
        return view(request, *args, **kwargs)
    return wrapper

def blocked_required(view):
    @login_required
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if request.user.access_code > 0:
            return unauthorized_response(request, request.user.dashboard)
        
        return view(request, *args, **kwargs)
    return wrapper


def applicant_only(view):
    @login_required
    def wrapper(request, *args, **kwargs):
        user = request.user

        if user.access_code != 1:
            messages.info(request, 'This page is only accessible to applicants.')
            return unauthorized_response(request, 'official:dashboard')

        if not user.registration_fee_payment:
            messages.info(request, 'You need to pay registration fee')
            return unauthorized_response(request, 'payment:registration-fee')
        return view(request, *args, **kwargs)
    return wrapper

def complete_profile_required(view):
    @applicant_only
    def wrapper(request, *args, **kwargs):
        profile_error_messages:list = request.user.profile_error_messages

        for message in profile_error_messages:
            messages.info(request, message)
                
        if profile_error_messages:
            return unauthorized_response(request, 'applicant:profile')
        return view(request, *args, **kwargs)
    return wrapper

def officials_only(admin_only=False, main_admin_only=False):
    def officials_deco(view):
        @login_required
        def wrapper(request, *args, **kwargs):
            user = request.user

            if user.access_code < 2:
                messages.error(request, 'This page is for officials only.')
                logout(request)
                return unauthorized_response(request, 'auth:signin')

            if admin_only and user.access_code == 2:
                messages.info(request, 'This page is for admins only.')
                return unauthorized_response(request, user.dashboard)
             
            if main_admin_only and user.access_code < 4:
                messages.info(request, 'This page is for main admins only.')
                return unauthorized_response(request, user.dashboard)
            return view(request, *args, **kwargs)
        return wrapper
    return officials_deco