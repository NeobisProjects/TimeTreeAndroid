from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_message(email, html, *kwargs):
    html_message = render_to_string(html, *kwargs)
    message = strip_tags(html_message)
    send_mail(
        'Neobis Clubs Application',
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=html_message
    )


def send_greeting_mail(email):
    user = User.objects.get(email=email)
    user.is_active = True
    password = User.objects.make_random_password(length=12)
    user.set_password(password)
    user.save()

    send_message(email, 'greeting_mail.html', {'email': email, 'password': password})
