"""
Notification models for CHAGUA E-Commerce Platform.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User


class Notification(models.Model):
    """User notifications."""

    TYPE_CHOICES = [
        ('ORDER_CREATED', 'Order Created'),
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('ORDER_SHIPPED', 'Order Shipped'),
        ('ORDER_DELIVERED', 'Order Delivered'),
        ('ORDER_CANCELLED', 'Order Cancelled'),
        ('PAYMENT_RECEIVED', 'Payment Received'),
        ('NEW_MESSAGE', 'New Message'),
        ('SUBSCRIPTION_EXPIRING', 'Subscription Expiring'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name=_('User'))
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name=_('Type'))
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    message = models.TextField(verbose_name=_('Message'))
    is_read = models.BooleanField(default=False, verbose_name=_('Read'))
    link = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Link'))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user}"
