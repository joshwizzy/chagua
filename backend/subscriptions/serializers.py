"""
Serializers for subscriptions.
"""
from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for subscriptions."""

    days_remaining = serializers.IntegerField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'status', 'start_date', 'end_date', 'price', 'currency',
                  'days_remaining', 'is_active', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']
