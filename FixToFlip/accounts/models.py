from django.db import models

from FixToFlip.choices import UserRoles


class BaseAccount(models.Model):
    role = models.CharField(
        max_length=10,
        choices=UserRoles.choices,
        blank=False,
        null=False,
    )

    username = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        unique=True,
    )

    email = models.EmailField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )

    first_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    last_name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )

    last_login = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    last_activity = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return self.username
