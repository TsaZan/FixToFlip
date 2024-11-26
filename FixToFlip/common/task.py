from celery import shared_task
from django.core.mail import send_mail

from FixToFlip import settings


@shared_task
def contact_form_mail(message):
    send_mail(
        subject='Fix To Flip Contact Form!',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.ADMIN_EMAIL]
    )
