"""
Serializers for payment processing.
"""
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments."""

    class Meta:
        model = Payment
        fields = ['id', 'order', 'payment_method', 'amount', 'currency', 'status',
                  'transaction_id', 'phone_number', 'reference_number', 'created_at', 'completed_at']
        read_only_fields = ['id', 'status', 'transaction_id', 'created_at', 'completed_at']
