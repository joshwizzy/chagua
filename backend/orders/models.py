"""
Order models for CHAGUA E-Commerce Platform.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db.models import Max
from datetime import datetime
import random
import string
from users.models import User, DeliveryAddress
from products.models import Product, ProductVariant


def generate_tracking_number():
    """
    Generate unique tracking number in format: CHAGUA-YYYYMMDD-XXXX
    Where XXXX is a sequential number for the day.
    """
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
    prefix = f'CHAGUA-{date_str}'

    # Get the last order for today
    last_order = Order.objects.filter(
        tracking_number__startswith=prefix
    ).aggregate(Max('tracking_number'))['tracking_number__max']

    if last_order:
        # Extract the sequential number and increment
        last_seq = int(last_order.split('-')[-1])
        new_seq = last_seq + 1
    else:
        # First order of the day
        new_seq = 1

    tracking_number = f'{prefix}-{new_seq:04d}'
    return tracking_number


def generate_randomized_tracking_number():
    """
    Generate unique tracking number with randomization: CHAGUA-YYYYMMDD-XXXX
    Where XXXX is a random alphanumeric string.
    """
    today = datetime.now()
    date_str = today.strftime('%Y%m%d')
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    tracking_number = f'CHAGUA-{date_str}-{random_suffix}'

    # Ensure uniqueness
    while Order.objects.filter(tracking_number=tracking_number).exists():
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        tracking_number = f'CHAGUA-{date_str}-{random_suffix}'

    return tracking_number


class Order(models.Model):
    """Order model."""

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed by Seller'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    # Order identification
    tracking_number = models.CharField(max_length=50, unique=True, editable=False, verbose_name=_('Tracking Number'))

    # Parties involved
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='orders', verbose_name=_('Buyer'))
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales', verbose_name=_('Seller'))

    # Delivery information
    delivery_address = models.ForeignKey(
        DeliveryAddress,
        on_delete=models.PROTECT,
        related_name='orders',
        verbose_name=_('Delivery Address')
    )

    # Order details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name=_('Status'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_('Total Amount'))
    currency = models.CharField(max_length=3, default='UGX', verbose_name=_('Currency'))

    # Payment details
    payment_method = models.CharField(max_length=50, verbose_name=_('Payment Method'))
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PAID', 'Paid'),
            ('FAILED', 'Failed'),
            ('REFUNDED', 'Refunded'),
        ],
        default='PENDING',
        verbose_name=_('Payment Status')
    )

    # Shipping information
    courier_receipt_photo = models.ImageField(
        upload_to='courier_receipts/',
        blank=True,
        null=True,
        verbose_name=_('Courier Receipt Photo')
    )
    estimated_delivery_date = models.DateField(blank=True, null=True, verbose_name=_('Estimated Delivery Date'))
    actual_delivery_date = models.DateTimeField(blank=True, null=True, verbose_name=_('Actual Delivery Date'))

    # Notes
    buyer_notes = models.TextField(blank=True, null=True, verbose_name=_('Buyer Notes'))
    seller_notes = models.TextField(blank=True, null=True, verbose_name=_('Seller Notes'))
    admin_notes = models.TextField(blank=True, null=True, verbose_name=_('Admin Notes'))

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    confirmed_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Confirmed At'))
    shipped_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Shipped At'))
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Delivered At'))
    cancelled_at = models.DateTimeField(blank=True, null=True, verbose_name=_('Cancelled At'))

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['buyer', 'status']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['tracking_number']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"Order {self.tracking_number}"

    def save(self, *args, **kwargs):
        # Generate tracking number if not exists
        if not self.tracking_number:
            # Use regular sequential tracking number
            # To use randomized, change to: generate_randomized_tracking_number()
            self.tracking_number = generate_tracking_number()
        super().save(*args, **kwargs)

    def mark_as_confirmed(self):
        """Mark order as confirmed by seller."""
        if self.status == 'PENDING':
            self.status = 'CONFIRMED'
            self.confirmed_at = datetime.now()
            self.save()
            return True
        return False

    def mark_as_shipped(self):
        """Mark order as shipped."""
        if self.status in ['CONFIRMED', 'PROCESSING']:
            self.status = 'SHIPPED'
            self.shipped_at = datetime.now()
            self.save()
            return True
        return False

    def mark_as_delivered(self):
        """Mark order as delivered."""
        if self.status == 'SHIPPED':
            self.status = 'DELIVERED'
            self.delivered_at = datetime.now()
            self.save()
            return True
        return False

    def cancel_order(self):
        """Cancel the order."""
        if self.status not in ['DELIVERED', 'CANCELLED']:
            self.status = 'CANCELLED'
            self.cancelled_at = datetime.now()
            self.save()
            return True
        return False


class OrderItem(models.Model):
    """Individual items in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name=_('Product'))
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('Variant')
    )

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name=_('Quantity'))
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_('Unit Price'))
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_('Subtotal'))

    # Snapshot of product details at time of order
    product_name = models.CharField(max_length=255, verbose_name=_('Product Name'))
    product_description = models.TextField(verbose_name=_('Product Description'))

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in {self.order.tracking_number}"

    def save(self, *args, **kwargs):
        # Calculate subtotal
        self.subtotal = self.unit_price * self.quantity

        # Save snapshot of product details
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_description:
            self.product_description = self.product.description

        super().save(*args, **kwargs)


class Cart(models.Model):
    """Shopping cart for users."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name=_('User'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart')
        verbose_name_plural = _('Carts')

    def __str__(self):
        return f"Cart of {self.user.get_full_name()}"

    def get_total(self):
        """Calculate total amount of items in cart."""
        return sum(item.get_subtotal() for item in self.items.all())

    def get_items_count(self):
        """Get total number of items in cart."""
        return sum(item.quantity for item in self.items.all())

    def clear(self):
        """Clear all items from cart."""
        self.items.all().delete()


class CartItem(models.Model):
    """Individual items in shopping cart."""

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name=_('Cart'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_('Product'))
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_('Variant')
    )
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name=_('Quantity'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Cart Item')
        verbose_name_plural = _('Cart Items')
        unique_together = ['cart', 'product', 'variant']

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart"

    def get_unit_price(self):
        """Get the unit price including variant adjustment."""
        price = self.product.price
        if self.variant:
            price += self.variant.price_adjustment
        return price

    def get_subtotal(self):
        """Calculate subtotal for this cart item."""
        return self.get_unit_price() * self.quantity


class OrderStatusHistory(models.Model):
    """Track order status changes."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history', verbose_name=_('Order'))
    old_status = models.CharField(max_length=20, verbose_name=_('Old Status'))
    new_status = models.CharField(max_length=20, verbose_name=_('New Status'))
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('Changed By'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Notes'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))

    class Meta:
        verbose_name = _('Order Status History')
        verbose_name_plural = _('Order Status Histories')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.order.tracking_number}: {self.old_status} → {self.new_status}"
