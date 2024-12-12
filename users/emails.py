from django.urls import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.conf import settings
from app.token import generate_token


def bssb_send_email(subject, message, recipient_list) -> bool:
    plain_message = strip_tags(message)
    return send_mail(
        subject, plain_message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        html_message=message,
        #fail_silently=True
    )


def send_activation_email(request, user) -> bool:
    mail_subject = 'Activate Your Account'
    token = generate_token(user.email)
    activation_link = reverse('user:activate', kwargs={
        'token': token
    })
    activation_link = request.build_absolute_uri(activation_link)
    message = render_to_string('email/activate-account.html', {
        'user': user,
        'activation_link': activation_link 
    })
    email_sent = bssb_send_email(mail_subject, message, [user.email])

    if email_sent: 
        msg = f"Dear {user}, please go to your email address to activate your account."
        messages.success(request, msg)
        return True
    
    messages.error(
        request, 
        f'Problem sending activation email to {user.email}, check if you typed it correctly.'
    )

    return False

def send_recovery_email(request, user) -> bool:
    mail_subject = 'Recover Your Account'
    token = generate_token(user.email)
    recovery_link = reverse('user:reset-password', kwargs={
        'token': token
    })
    recovery_link = request.build_absolute_uri(recovery_link)
    message = render_to_string('email/recover-account.html', {
        'user': user,
        'recovery_link': recovery_link 
    })
    
    email_sent = bssb_send_email(mail_subject, message, [user.email])
    
    if email_sent: 
        msg = f"Dear {user}, please go to your email address to recover your account."
        messages.success(
            request, msg)
        return True
    
    messages.error(
        request, 
        f'Problem sending recovery email to {user.email}, check if account really exists.'
    )

    return False