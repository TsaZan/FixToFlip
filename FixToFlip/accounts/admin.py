from django.contrib import admin
from unfold.admin import ModelAdmin
from FixToFlip.accounts.models import BaseAccount, Profile


@admin.register(BaseAccount)
class AccountsAdmin(ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name',)
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )


@admin.register(Profile)
class Profile(ModelAdmin):
    list_display = ('user', 'profile_type', 'preferred_currency', 'user_location')
    search_fields = ('user_location',)
    list_filter = ('profile_type', 'preferred_currency',)
    fieldsets = (
        (None, {
            'fields': ('profile_type', 'profile_picture')
        }),
        ('Links', {
            'fields': ('company_url',)
        }),
        ('Personal Info', {
            'fields': ('user_location', 'phone_number')
        }),
        ('Company Info', {
            'fields': ('company_name', 'company_location_country', 'company_phone')
        }),
        ('Preferences', {
            'fields': ('preferred_currency',)
        }),
    )
