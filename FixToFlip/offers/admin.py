from django.contrib import admin

from FixToFlip.offers.models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    pass