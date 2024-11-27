from django.db import models
from cloudinary.models import CloudinaryField
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from FixToFlip.choices import OfferStatusChoices


class Offer(models.Model):
    title = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    image = CloudinaryField('image', blank=True, null=True, )

    video = CloudinaryField('video', resource_type='video', blank=True, null=True, )

    price = MoneyField(max_digits=10, decimal_places=2, default=Money(0, 'EUR'), blank=True, null=True, )

    offer_validity = models.DateField(blank=True, null=True, )

    brokerage_commission = MoneyField(max_digits=8, decimal_places=2, default=Money(0, 'EUR'), blank=True, null=True, )

    offer_status = models.CharField(
        max_length=15,
        choices=OfferStatusChoices.choices,
        blank=True, null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, null=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True, blank=True, null=True,
    )

    rooms = models.PositiveIntegerField(blank=True, null=True, )

    property_size = models.PositiveIntegerField(blank=True, null=True, )

    def __str__(self):
        return self.title
