from allauth.account.models import EmailAddress
from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
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

    unverified_users_list = list(unverified_users)
    unverified_users_data = [f"{user.username} <{user.email}>" for user in unverified_users_list]
    message = "Today we delete:\n" + "\n".join(unverified_users_data)

    send_mail(
        subject="Deleted Users",
        message=message,
        from_email="fixtoflips@gmail.com",
        recipient_list=["fixtoflips@gmail.com"]
    )

    unverified_users.delete()
