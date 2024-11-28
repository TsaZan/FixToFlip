from decimal import Decimal

from django.db import models
from cloudinary.models import CloudinaryField
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MinMoneyValidator
from djmoney.money import Money

from FixToFlip.choices import OfferStatusChoices
from FixToFlip.properties.models import Property


class Offer(models.Model):
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
        max_digits=10,
        decimal_places=2,
        default=Money(0, 'EUR'),
        validators=[MinMoneyValidator(Decimal(0), message='Price cannot be negative.')],
        blank=True,
        null=True,
    )

    offer_status = models.CharField(
        max_length=15,
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
        max_digits=10,
        default=Money(0, 'EUR'),
        decimal_places=2,
        blank=True,
        null=True,
    )

    sold_date = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title


class OfferImages(models.Model):
    related_property = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='images'
    )

    image = CloudinaryField('image', resource_type='image')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class OfferVideos(models.Model):
    related_property = models.ForeignKey(
        to=Offer,
        on_delete=models.CASCADE,
        related_name='videos'
    )

    video = CloudinaryField('video', resource_type='video')
    uploaded_at = models.DateTimeField(auto_now_add=True)