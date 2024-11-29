from decimal import Decimal

from django.db import models
from cloudinary.models import CloudinaryField
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money

from FixToFlip.choices import OfferStatusChoices
from FixToFlip.properties.models import Property


class Offer(models.Model):
    MAX_DIGITS = 10
    MAX_DECIMAL_PLACES = 2

    class Meta:
        verbose_name = 'Offer'
        verbose_name_plural = 'Offers'
        ordering = ['-updated_at']

    title = models.CharField(
        max_length=100,
    )

    featured_image = CloudinaryField(
        'image',
        resource_type='image',
        blank=True,
        null=True,
    )

    description = models.TextField()

    listed_price = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0), message='Price cannot be negative.')],
        blank=True,
        null=True,
    )

    offer_status = models.CharField(
        max_length=6,
        choices=OfferStatusChoices.choices,
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
    )

    listed_property = models.ForeignKey(
        to=Property,
        related_name='listed_for_sales',
        on_delete=models.SET_NULL,
        null=True,
    )

    actual_sold_price = MoneyField(
        max_digits=MAX_DIGITS,
        decimal_places=MAX_DECIMAL_PLACES,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0), message='Price cannot be negative.')],
        blank=True,
        null=True,
    )

    sold_date = models.DateField(
        blank=True,
        null=True,
    )

    is_published = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )

    def __str__(self):
        return self.title


class OfferImages(models.Model):
    class Meta:
        verbose_name = 'Offer Image'
        verbose_name_plural = 'Offer Images'
        ordering = ['-uploaded_at']

    related_property = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = CloudinaryField('image', resource_type='image')

    uploaded_at = models.DateTimeField(auto_now_add=True)


class OfferVideos(models.Model):
    class Meta:
        verbose_name = 'Offer Video'
        verbose_name_plural = 'Offer Videos'
        ordering = ['-uploaded_at']

    related_property = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='videos'
    )

    video = CloudinaryField('video', resource_type='video')

    uploaded_at = models.DateTimeField(auto_now_add=True)