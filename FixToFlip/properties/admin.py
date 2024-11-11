from django.contrib import admin
from .models import Property, PropertyForSale, PropertyFinancialInformation


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        'property_name', 'country', 'city', 'property_type',
        'bedrooms', 'bathrooms', 'property_size', 'year_of_built', 'owner', 'created_at'
    )
    search_fields = ('property_name', 'country', 'city', 'address', 'owner__username')
    list_filter = ('property_type', 'property_condition', 'year_of_built', 'created_at')
    ordering = ['-created_at']
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('property_name', 'property_description', 'country', 'city', 'address', 'property_type')
        }),
        ('Details', {
            'fields': ('bedrooms', 'bathrooms', 'floor', 'year_of_built', 'property_size', 'bought_date')
        }),
        ('Additional Info', {
            'fields': ('notes', 'property_condition',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PropertyForSale)
class PropertyForSaleAdmin(admin.ModelAdmin):
    list_display = ('property_name', 'listed_price', 'is_furnished', 'listed_date')
    search_fields = ('property_name', 'list_description')
    list_filter = ('is_furnished', 'listed_date')
    readonly_fields = ('listed_date',)
    fieldsets = (
        ('Basic Info', {
            'fields': ('property_name', 'listed_price', 'is_furnished', 'list_description', 'listed_property')
        }),
        ('Date Info', {
            'fields': ('listed_date',)
        }),
    )


@admin.register(PropertyFinancialInformation)
class PropertyFinancialInformationAdmin(admin.ModelAdmin):
    list_display = ('initial_price', 'repair_cost')
    search_fields = ('initial_price',)
