from allauth.account.models import EmailAddress
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()


@shared_task
def send_email_confirmation_task(user_id):
    user = User.objects.get(id=user_id)

    email_address, created = EmailAddress.objects.get_or_create(
        user=user,
        email=user.email,
        defaults={'primary': True, 'verified': False},
    )

    email_address.send_confirmation()


@shared_task
def delete_unverified_users():
    expire_date = now() - timedelta(days=7)
    unverified_users = User.objects.filter(
        is_active=True,
        date_joined__lt=expire_date,
        emailaddress__verified=False
    )

    unverified_users.delete()
