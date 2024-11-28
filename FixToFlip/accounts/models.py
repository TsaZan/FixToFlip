from cities_light.models import Country
from cloudinary.models import CloudinaryField
from django.db import models
from django.contrib.auth.models import AbstractUser
from djmoney.settings import CURRENCY_CHOICES
from phonenumber_field.modelfields import PhoneNumberField

from FixToFlip.accounts.managers import BaseAccountManager
from FixToFlip.choices import ProfileTypes


class BaseAccount(AbstractUser):
    last_login = models.DateTimeField(
        auto_now_add=True,
    )

    objects = BaseAccountManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    class Meta:
        ordering = ['user']
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

    user = models.OneToOneField(
        to=BaseAccount,
        on_delete=models.CASCADE,
        primary_key=True
    )

    profile_type = models.CharField(
        max_length=10,
        choices=ProfileTypes,
        null=True,
        blank=True,
    )

    phone_number = PhoneNumberField(blank=True)

    preferred_currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='EUR',
        null=True,
        blank=True
    )

    user_location = models.ForeignKey(
        to=Country,
        null=True,
        blank=True,
        on_delete=models.CASCADE,

    )

    company_name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )

    company_phone = PhoneNumberField(blank=True)

    company_location_country = models.ForeignKey(
        to=Country,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='company_location_profile'
    )

    company_url = models.URLField(
        null=True,
        blank=True,
    )

    profile_picture = CloudinaryField(
        'image',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.user.username} Profile"
