from django.contrib import admin
from unfold.admin import ModelAdmin
from FixToFlip.credits.models import Credit, CreditPayment


@admin.register(Credit)
class CreditAdmin(ModelAdmin):
    list_display = (
        "bank_name",
        "credit_amount",
        "credit_term",
        "credit_interest",
        "monthly_payment",
    )
    search_fields = ("bank_name",)


@admin.register(CreditPayment)
class CreditPaymentAdmin(ModelAdmin):
    list_display = (
        "payment_date",
        "principal_amount",
        "interest_amount",
    )
    search_fields = ("credit",)
