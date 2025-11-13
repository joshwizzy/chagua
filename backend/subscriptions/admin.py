from django.contrib import admin
from .models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'created_at']
    list_filter = ['plan', 'status', 'created_at']
    search_fields = ['user__phone_number', 'user__first_name']
