"""
Serializers for order management.
"""
from rest_framework import serializers
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem, Cart, CartItem, OrderStatusHistory
from products.models import Product, ProductVariant
from users.models import DeliveryAddress


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for order items."""

    product_name = serializers.CharField(read_only=True)
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'product_image', 'variant', 'quantity',
                  'unit_price', 'subtotal', 'product_description']
        read_only_fields = ['id', 'unit_price', 'subtotal', 'product_name', 'product_description']

    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image and 'request' in self.context:
            return self.context['request'].build_absolute_uri(primary_image.image.url)
        return None


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for order listing (summary view)."""

    buyer_name = serializers.CharField(source='buyer.get_full_name', read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'tracking_number', 'buyer_name', 'seller_name', 'status', 'payment_status',
                  'total_amount', 'currency', 'items_count', 'created_at']
        read_only_fields = ['id', 'tracking_number', 'created_at']

    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for order detail view."""

    buyer = serializers.SerializerMethodField()
    seller = serializers.SerializerMethodField()
    delivery_address = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'tracking_number', 'buyer', 'seller', 'delivery_address', 'items',
                  'status', 'payment_method', 'payment_status', 'total_amount', 'currency',
                  'courier_receipt_photo', 'estimated_delivery_date', 'actual_delivery_date',
                  'buyer_notes', 'seller_notes', 'created_at', 'updated_at', 'confirmed_at',
                  'shipped_at', 'delivered_at', 'cancelled_at']
        read_only_fields = ['id', 'tracking_number', 'buyer', 'seller', 'created_at', 'updated_at',
                            'confirmed_at', 'shipped_at', 'delivered_at', 'cancelled_at']

    def get_buyer(self, obj):
        return {
            'id': obj.buyer.id,
            'name': obj.buyer.get_full_name(),
            'phone': str(obj.buyer.phone_number),
            'email': obj.buyer.email,
        }

    def get_seller(self, obj):
        return {
            'id': obj.seller.id,
            'name': obj.seller.get_full_name(),
            'phone': str(obj.seller.phone_number),
            'email': obj.seller.email,
        }

    def get_delivery_address(self, obj):
        return {
            'recipient_name': obj.delivery_address.recipient_name,
            'phone': str(obj.delivery_address.phone_number),
            'country': obj.delivery_address.country,
            'city': obj.delivery_address.city,
            'address_line1': obj.delivery_address.address_line1,
            'address_line2': obj.delivery_address.address_line2,
            'postal_code': obj.delivery_address.postal_code,
        }


class OrderCreateSerializer(serializers.Serializer):
    """Serializer for creating orders from cart."""

    delivery_address_id = serializers.IntegerField()
    payment_method = serializers.CharField()
    buyer_notes = serializers.CharField(required=False, allow_blank=True)

    def validate_delivery_address_id(self, value):
        try:
            address = DeliveryAddress.objects.get(id=value, user=self.context['request'].user)
            return address
        except DeliveryAddress.DoesNotExist:
            raise serializers.ValidationError("Invalid delivery address.")

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        delivery_address = validated_data['delivery_address_id']
        payment_method = validated_data['payment_method']
        buyer_notes = validated_data.get('buyer_notes', '')

        # Get user's cart
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Cart is empty.")

        if not cart.items.exists():
            raise serializers.ValidationError("Cart is empty.")

        # Group cart items by seller
        seller_items = {}
        for cart_item in cart.items.select_related('product__seller', 'variant'):
            seller = cart_item.product.seller
            if seller not in seller_items:
                seller_items[seller] = []
            seller_items[seller].append(cart_item)

        # Create separate orders for each seller
        orders = []
        for seller, items in seller_items.items():
            # Calculate total
            total_amount = sum(item.get_subtotal() for item in items)

            # Get currency from user profile
            currency = user.profile.preferred_currency if hasattr(user, 'profile') else 'UGX'

            # Create order
            order = Order.objects.create(
                buyer=user,
                seller=seller,
                delivery_address=delivery_address,
                payment_method=payment_method,
                total_amount=total_amount,
                currency=currency,
                buyer_notes=buyer_notes,
            )

            # Create order items
            for cart_item in items:
                unit_price = cart_item.get_unit_price()

                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    variant=cart_item.variant,
                    quantity=cart_item.quantity,
                    unit_price=unit_price,
                )

                # Update product stock and sales count
                cart_item.product.reduce_stock(cart_item.quantity)
                cart_item.product.increment_sales()

            orders.append(order)

        # Clear cart
        cart.clear()

        return orders


class OrderStatusUpdateSerializer(serializers.Serializer):
    """Serializer for updating order status."""

    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
    notes = serializers.CharField(required=False, allow_blank=True)
    courier_receipt_photo = serializers.ImageField(required=False)
    estimated_delivery_date = serializers.DateField(required=False)

    def validate(self, attrs):
        order = self.context.get('order')
        new_status = attrs['status']
        user = self.context['request'].user

        # Validate status transitions
        if order.status == 'DELIVERED' and new_status != 'DELIVERED':
            raise serializers.ValidationError("Cannot change status of delivered order.")

        if order.status == 'CANCELLED' and new_status != 'CANCELLED':
            raise serializers.ValidationError("Cannot change status of cancelled order.")

        # Only seller can confirm or ship
        if new_status in ['CONFIRMED', 'SHIPPED'] and user != order.seller and user.role != 'ADMIN':
            raise serializers.ValidationError("Only the seller can update to this status.")

        return attrs


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for cart items."""

    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.SerializerMethodField()
    unit_price = serializers.SerializerMethodField()
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image', 'variant',
                  'quantity', 'unit_price', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_product_image(self, obj):
        primary_image = obj.product.images.filter(is_primary=True).first()
        if primary_image and 'request' in self.context:
            return self.context['request'].build_absolute_uri(primary_image.image.url)
        return None

    def get_unit_price(self, obj):
        return obj.get_unit_price()

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):
    """Serializer for shopping cart."""

    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total', 'items_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj):
        return obj.get_total()

    def get_items_count(self, obj):
        return obj.get_items_count()


class AddToCartSerializer(serializers.Serializer):
    """Serializer for adding items to cart."""

    product_id = serializers.IntegerField()
    variant_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
            return product
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found.")

    def validate_variant_id(self, value):
        if value:
            try:
                variant = ProductVariant.objects.get(id=value)
                return variant
            except ProductVariant.DoesNotExist:
                raise serializers.ValidationError("Product variant not found.")
        return None


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for order status history."""

    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'old_status', 'new_status', 'changed_by_name', 'notes', 'timestamp']
        read_only_fields = ['id', 'timestamp']
