"""
Payment models for CHAGUA E-Commerce Platform.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from orders.models import Order


class Payment(models.Model):
    """Payment transactions."""

    PAYMENT_METHOD_CHOICES = [
        ('CASH_ON_DELIVERY', 'Cash on Delivery'),
        ('AIRTEL_MONEY', 'Airtel Money'),
        ('MTN_MOBILE_MONEY', 'MTN Mobile Money'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]

    order = models.OneToOneField(Order, on_delete=models.PROTECT, related_name='payment', verbose_name=_('Order'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='payments', verbose_name=_('User'))

    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, verbose_name=_('Payment Method'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    currency = models.CharField(max_length=3, default='UGX', verbose_name=_('Currency'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name=_('Status'))

    # Transaction details
    transaction_id = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Transaction ID'))
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Number'))
    reference_number = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Reference Number'))

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment for {self.order.tracking_number}"
