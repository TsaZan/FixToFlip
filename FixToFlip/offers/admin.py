from django.contrib import admin
from unfold.admin import ModelAdmin

from FixToFlip.offers.models import Offer


@admin.register(Offer)
class OfferAdmin(ModelAdmin):
    list_display = ('listed_property', 'is_published', 'listed_price', 'created_at')
    search_fields = ('list_description',)
    list_filter = ('created_at', 'is_published',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Images & Videos', {
            'fields': ('featured_image',),
        }),
        ('Basic Info', {
            'fields': ('listed_price', 'title', 'description', 'listed_property', 'is_published')
        }),
        ('Date Info', {
            'fields': ('created_at',)
        }),
    )


