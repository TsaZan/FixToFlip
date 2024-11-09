from django.contrib import admin

from FixToFlip.accounts.models import BaseAccount, Profile


@admin.register(BaseAccount)
class AccountsAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    pass
