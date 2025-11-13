"""
Subscription models for CHAGUA E-Commerce Platform.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.utils import timezone
from users.models import User


class Subscription(models.Model):
    """Seller subscriptions."""

    PLAN_CHOICES = [
        ('BASIC', 'Basic'),
        ('PRO', 'Pro'),
        ('PREMIUM', 'Premium'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', verbose_name=_('User'))
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, verbose_name=_('Plan'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name=_('Status'))

    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))

    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Price'))
    currency = models.CharField(max_length=3, default='UGX', verbose_name=_('Currency'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.plan}"

    def is_active(self):
        """Check if subscription is currently active."""
        return self.status == 'ACTIVE' and self.end_date >= timezone.now().date()

    def days_remaining(self):
        """Get days remaining in subscription."""
        if self.is_active():
            return (self.end_date - timezone.now().date()).days
        return 0
