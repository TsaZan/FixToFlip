from celery import shared_task
from django.core.mail import send_mail

from FixToFlip import settings


@shared_task
def contact_form_mail(name, email, message):
    subject = "[FixToFlip] Contact Form!"
    body = f"""
    From:
        {name}

    Message:
        {message}

    Email:
        {email}
    """
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_EMAIL],
    )
