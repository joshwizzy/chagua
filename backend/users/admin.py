"""
Admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, DeliveryAddress


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""

    list_display = ['phone_number', 'first_name', 'last_name', 'role', 'is_active', 'is_verified', 'date_joined']
    list_filter = ['role', 'is_active', 'is_verified', 'mfa_enabled']
    search_fields = ['phone_number', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']

    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions'),
        }),
        (_('Security'), {'fields': ('mfa_enabled', 'mfa_secret')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""

    list_display = ['user', 'country', 'city', 'preferred_language', 'preferred_currency']
    list_filter = ['country', 'preferred_language', 'preferred_currency']
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name', 'city']


@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    """Admin interface for DeliveryAddress model."""

    list_display = ['user', 'label', 'recipient_name', 'country', 'city', 'is_default']
    list_filter = ['country', 'is_default']
    search_fields = ['user__phone_number', 'recipient_name', 'city', 'address_line1']
