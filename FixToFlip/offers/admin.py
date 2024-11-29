# from django.contrib import admin
# from unfold.admin import ModelAdmin
#
# from FixToFlip.offers.models import Offer
#
#
# @admin.register(Offer)
# class OfferAdmin(ModelAdmin):
#     list_display = ('property_name', 'listed_price', 'is_furnished', 'listed_date')
#     search_fields = ('property_name', 'list_description')
#     list_filter = ('is_furnished', 'listed_date')
#     readonly_fields = ('listed_date',)
#     fieldsets = (
#         ('Basic Info', {
#             'fields': ('property_name', 'listed_price', 'is_furnished', 'list_description', 'listed_property')
#         }),
#         ('Date Info', {
#             'fields': ('listed_date',)
#         }),
#     )