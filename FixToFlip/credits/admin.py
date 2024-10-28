from django.contrib import admin

from FixToFlip.credits.models import Credit


# Register your models here.
@admin.register(Credit)
class CreditAdmin(admin.ModelAdmin):
    pass
