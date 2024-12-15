from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from app.token import generate_token

def get_full_link(request, user, view) -> str:
    token = generate_token(user.email)
    link = reverse(view, kwargs={'token': token})
    link = request.build_absolute_uri(link)
    return link

def bssb_send_email(subject:str, message:str, recipient_list:list[str], is_optional:bool=True) -> bool:
    plain_message = strip_tags(message)
    return send_mail(
        subject, plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        html_message=message,
        fail_silently=is_optional
    )

def send_login_verification_link(request, user) -> bool:
    mail_subject = 'Signin Verification Instructions'
    login_verification_link = get_full_link(request, user, 'auth:signin-verification')
    message = render_to_string('email/login-verification.html', {
        'user': user,
        'login_verification_link': login_verification_link 
    })

    if bssb_send_email(mail_subject, message, [user.email]): return True

    messages.error(
        request, 
        f'Problem sending login verification link to {user.email}, please try again later.'
    )

    return False

def send_activation_email(request, user) -> bool:
    mail_subject = 'Welcome to Borno State Scholarship Board'
    activation_link = get_full_link(request, user, 'auth:activate')
    message = render_to_string('email/activate-account.html', {
        'user': user,
        'activation_link': activation_link 
    })

    if bssb_send_email(mail_subject, message, [user.email]): return True

    messages.error(
        request, 
        f'Problem sending activation email to {user.email}, check if you typed it correctly.'
    )

    return False

def send_recovery_email(request, user) -> bool:
    mail_subject = 'Account Recovery Instructions'
    recovery_link = get_full_link(request, user, 'auth:reset-password')
    message = render_to_string('email/recover-account.html', {
        'user': user,
        'recovery_link': recovery_link 
    })
    
    if bssb_send_email(mail_subject, message, [user.email]): return True
    
    messages.error(
        request, 
        f'Problem sending recovery email to {user.email}, check if account really exists.'
    )

    return False