"""
Views for order management.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, Cart, CartItem, OrderStatusHistory
from .serializers import (
    OrderListSerializer,
    OrderDetailSerializer,
    OrderCreateSerializer,
    OrderStatusUpdateSerializer,
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
    OrderStatusHistorySerializer,
)
from products.models import Product


class OrderListView(generics.ListAPIView):
    """API endpoint for listing user's orders."""

    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Show orders where user is either buyer or seller
        return Order.objects.filter(
            Q(buyer=user) | Q(seller=user)
        ).select_related('buyer', 'seller').order_by('-created_at')


class BuyerOrderListView(generics.ListAPIView):
    """API endpoint for listing buyer's orders."""

    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).select_related('seller').order_by('-created_at')


class SellerOrderListView(generics.ListAPIView):
    """API endpoint for listing seller's orders (sales)."""

    serializer_class = OrderListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(seller=self.request.user).select_related('buyer').order_by('-created_at')


class OrderDetailView(generics.RetrieveAPIView):
    """API endpoint for viewing order details."""

    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'tracking_number'

    def get_queryset(self):
        user = self.request.user
        # Allow access if user is buyer, seller, or admin
        return Order.objects.filter(
            Q(buyer=user) | Q(seller=user) | Q(buyer__role='ADMIN')
        ).select_related('buyer', 'seller', 'delivery_address')


class OrderCreateView(generics.CreateAPIView):
    """API endpoint for creating orders from cart."""

    serializer_class = OrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        orders = serializer.save()

        # Return the created orders
        response_data = {
            'message': f'{len(orders)} order(s) created successfully.',
            'orders': [OrderListSerializer(order, context={'request': request}).data for order in orders]
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class OrderStatusUpdateView(generics.UpdateAPIView):
    """API endpoint for updating order status."""

    serializer_class = OrderStatusUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        # Allow sellers to update their sales, buyers to cancel their orders
        return Order.objects.filter(
            Q(seller=user) | Q(buyer=user) | Q(buyer__role='ADMIN')
        )

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'order': order, 'request': request})
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data['status']
        notes = serializer.validated_data.get('notes', '')
        old_status = order.status

        # Record status change in history
        OrderStatusHistory.objects.create(
            order=order,
            old_status=old_status,
            new_status=new_status,
            changed_by=request.user,
            notes=notes
        )

        # Update order status
        order.status = new_status

        # Update timestamps based on status
        if new_status == 'CONFIRMED' and not order.confirmed_at:
            order.confirmed_at = timezone.now()
        elif new_status == 'SHIPPED' and not order.shipped_at:
            order.shipped_at = timezone.now()
        elif new_status == 'DELIVERED' and not order.delivered_at:
            order.delivered_at = timezone.now()
        elif new_status == 'CANCELLED' and not order.cancelled_at:
            order.cancelled_at = timezone.now()

        # Update optional fields
        if 'courier_receipt_photo' in serializer.validated_data:
            order.courier_receipt_photo = serializer.validated_data['courier_receipt_photo']
        if 'estimated_delivery_date' in serializer.validated_data:
            order.estimated_delivery_date = serializer.validated_data['estimated_delivery_date']

        order.save()

        return Response(OrderDetailSerializer(order, context={'request': request}).data)


class OrderCancelView(generics.UpdateAPIView):
    """API endpoint for cancelling orders."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only buyers can cancel their own orders
        return Order.objects.filter(buyer=self.request.user)

    def update(self, request, *args, **kwargs):
        order = self.get_object()

        if order.status in ['DELIVERED', 'CANCELLED']:
            return Response(
                {'error': f'Cannot cancel order with status: {order.status}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Record cancellation in history
        OrderStatusHistory.objects.create(
            order=order,
            old_status=order.status,
            new_status='CANCELLED',
            changed_by=request.user,
            notes=request.data.get('reason', 'Cancelled by buyer')
        )

        order.cancel_order()

        return Response(
            {'message': 'Order cancelled successfully.'},
            status=status.HTTP_200_OK
        )


class CartView(generics.RetrieveAPIView):
    """API endpoint for viewing shopping cart."""

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    """API endpoint for adding items to cart."""

    serializer_class = AddToCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data['product_id']
        variant = serializer.validated_data.get('variant_id')
        quantity = serializer.validated_data['quantity']

        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if item already in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            variant=variant,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()

        return Response(
            CartSerializer(cart, context={'request': request}).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class UpdateCartItemView(generics.UpdateAPIView):
    """API endpoint for updating cart item quantity."""

    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        quantity = request.data.get('quantity')

        if not quantity or int(quantity) < 1:
            return Response(
                {'error': 'Quantity must be at least 1.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = int(quantity)
        cart_item.save()

        return Response(CartItemSerializer(cart_item, context={'request': request}).data)


class RemoveFromCartView(generics.DestroyAPIView):
    """API endpoint for removing items from cart."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class ClearCartView(generics.GenericAPIView):
    """API endpoint for clearing the cart."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            cart = Cart.objects.get(user=request.user)
            cart.clear()
            return Response({'message': 'Cart cleared successfully.'}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'message': 'Cart is already empty.'}, status=status.HTTP_200_OK)


class OrderStatusHistoryView(generics.ListAPIView):
    """API endpoint for viewing order status history."""

    serializer_class = OrderStatusHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        tracking_number = self.kwargs['tracking_number']
        order = get_object_or_404(Order, tracking_number=tracking_number)

        # Check if user has access to this order
        user = self.request.user
        if order.buyer != user and order.seller != user and user.role != 'ADMIN':
            return OrderStatusHistory.objects.none()

        return OrderStatusHistory.objects.filter(order=order).select_related('changed_by')


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def track_order(request, tracking_number):
    """Track order by tracking number."""
    try:
        order = Order.objects.get(tracking_number=tracking_number)

        # Check if user has access to this order
        if order.buyer != request.user and order.seller != request.user and request.user.role != 'ADMIN':
            return Response(
                {'error': 'You do not have permission to view this order.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = OrderDetailSerializer(order, context={'request': request})
        return Response(serializer.data)

    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
