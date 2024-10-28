from django.contrib import admin

from FixToFlip.properties.models import Property, PropertyFinancialInformation, PropertyForSale, PropertyExpense


# Register your models here.

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    pass

@admin.register(PropertyFinancialInformation)
class PropertyFinancialInformationAdmin(admin.ModelAdmin):
    pass

@admin.register(PropertyForSale)
class PropertiesForSalesAdmin(admin.ModelAdmin):
    pass

@admin.register(PropertyExpense)
class PropertyExpenseAdmin(admin.ModelAdmin):
    pass