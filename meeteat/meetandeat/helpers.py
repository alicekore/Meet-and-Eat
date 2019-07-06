from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from meetandeat.tokens import account_activation_token
from meeteat import settings


def send_activation_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('emails/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    print(message)
    to_email = user.email
    email = EmailMessage(
        mail_subject,
        message,
        to=[to_email],
        from_email='Meet-and-Eat',
    )
    if settings.EMAIL_ENABLED:
        sent_emails = email.send(fail_silently=True)
    else:
        sent_emails = 1
    return sent_emails


def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Password reset'
    message = render_to_string('emails/acc_password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    print(message)
    if user.is_email_confirmed:
        to_email = user.email
    else:
        to_email = user.old_email

    email = EmailMessage(
        mail_subject,
        message,
        to=[to_email],
        from_email='Meet-and-Eat',
    )
    if settings.EMAIL_ENABLED:
        sent_emails = email.send(fail_silently=True)
    else:
        sent_emails = 1
    return sent_emails
