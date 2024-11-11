from django.contrib import admin

from FixToFlip.credits.models import Credit, CreditPayment


# Register your models here.
@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    pass


@admin.register(CreditPayment)
class CreditPaymentAdmin(admin.ModelAdmin):
    pass
