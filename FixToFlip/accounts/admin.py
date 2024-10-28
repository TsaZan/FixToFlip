from django.contrib import admin

from FixToFlip.accounts.models import BaseAccount


@admin.register(BaseAccount)
class AccountsAdmin(admin.ModelAdmin):
    pass

