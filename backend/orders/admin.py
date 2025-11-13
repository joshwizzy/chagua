"""
Admin configuration for orders app.
"""
from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, OrderStatusHistory


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items."""

    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_description', 'unit_price', 'subtotal']
    fields = ['product', 'variant', 'quantity', 'unit_price', 'subtotal']


class OrderStatusHistoryInline(admin.TabularInline):
    """Inline admin for order status history."""

    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['old_status', 'new_status', 'changed_by', 'notes', 'timestamp']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""

    list_display = ['tracking_number', 'buyer', 'seller', 'status', 'payment_status',
                    'total_amount', 'currency', 'created_at']
    list_filter = ['status', 'payment_status', 'created_at', 'currency']
    search_fields = ['tracking_number', 'buyer__phone_number', 'buyer__first_name',
                     'seller__phone_number', 'seller__first_name']
    readonly_fields = ['tracking_number', 'created_at', 'updated_at', 'confirmed_at',
                       'shipped_at', 'delivered_at', 'cancelled_at']
    inlines = [OrderItemInline, OrderStatusHistoryInline]

    fieldsets = (
        ('Order Information', {
            'fields': ('tracking_number', 'buyer', 'seller', 'delivery_address')
        }),
        ('Order Details', {
            'fields': ('status', 'payment_method', 'payment_status', 'total_amount', 'currency')
        }),
        ('Shipping', {
            'fields': ('courier_receipt_photo', 'estimated_delivery_date', 'actual_delivery_date')
        }),
        ('Notes', {
            'fields': ('buyer_notes', 'seller_notes', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'confirmed_at', 'shipped_at', 'delivered_at', 'cancelled_at')
        }),
    )


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items."""

    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin interface for Cart model."""

    list_display = ['user', 'created_at', 'updated_at']
    search_fields = ['user__phone_number', 'user__first_name', 'user__last_name']
    inlines = [CartItemInline]
