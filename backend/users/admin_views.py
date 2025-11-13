"""
Admin-specific views for platform management.
"""
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Sum, Count, Q, Avg
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from users.models import User, UserProfile
from products.models import Product
from orders.models import Order
from subscriptions.models import Subscription
from reviews.models import ProductReview, SellerReview

User = get_user_model()


class IsAdminUser(permissions.BasePermission):
    """Custom permission to only allow admin users."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'ADMIN'


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_statistics(request):
    """Get platform-wide statistics for admin dashboard."""

    # User statistics
    total_users = User.objects.count()
    buyers = User.objects.filter(role='BUYER').count()
    sellers = User.objects.filter(role='SELLER').count()
    admins = User.objects.filter(role='ADMIN').count()

    # New users in last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_users_30d = User.objects.filter(date_joined__gte=thirty_days_ago).count()

    # Product statistics
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    featured_products = Product.objects.filter(is_featured=True).count()
    out_of_stock = Product.objects.filter(availability='OUT_OF_STOCK').count()

    # Order statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='PENDING').count()
    completed_orders = Order.objects.filter(status='DELIVERED').count()
    cancelled_orders = Order.objects.filter(status='CANCELLED').count()

    # Revenue statistics
    total_revenue = Order.objects.filter(
        status__in=['CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Subscription statistics
    active_subscriptions = Subscription.objects.filter(status='ACTIVE').count()
    expired_subscriptions = Subscription.objects.filter(status='EXPIRED').count()
    subscription_revenue = Subscription.objects.filter(
        status='ACTIVE'
    ).aggregate(total=Sum('price'))['total'] or 0

    # Review statistics
    total_reviews = ProductReview.objects.count()
    avg_rating = ProductReview.objects.filter(
        is_approved=True
    ).aggregate(avg=Avg('rating'))['avg'] or 0

    # Recent activity (last 7 days)
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_orders = Order.objects.filter(created_at__gte=seven_days_ago).count()
    recent_products = Product.objects.filter(created_at__gte=seven_days_ago).count()
    recent_users = User.objects.filter(date_joined__gte=seven_days_ago).count()

    return Response({
        'users': {
            'total': total_users,
            'buyers': buyers,
            'sellers': sellers,
            'admins': admins,
            'new_30d': new_users_30d
        },
        'products': {
            'total': total_products,
            'active': active_products,
            'featured': featured_products,
            'out_of_stock': out_of_stock
        },
        'orders': {
            'total': total_orders,
            'pending': pending_orders,
            'completed': completed_orders,
            'cancelled': cancelled_orders
        },
        'revenue': {
            'total_sales': float(total_revenue),
            'subscriptions': float(subscription_revenue),
            'total': float(total_revenue + subscription_revenue)
        },
        'subscriptions': {
            'active': active_subscriptions,
            'expired': expired_subscriptions
        },
        'reviews': {
            'total': total_reviews,
            'average_rating': float(avg_rating)
        },
        'recent_activity': {
            'orders': recent_orders,
            'products': recent_products,
            'users': recent_users
        }
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_users_list(request):
    """List all users with filtering."""

    # Get query parameters
    role = request.query_params.get('role')
    search = request.query_params.get('search')
    is_active = request.query_params.get('is_active')

    # Base queryset
    queryset = User.objects.all().select_related('profile')

    # Apply filters
    if role:
        queryset = queryset.filter(role=role)
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(email__icontains=search)
        )
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')

    # Serialize data
    users_data = []
    for user in queryset[:100]:  # Limit to 100 for performance
        users_data.append({
            'id': user.id,
            'phone_number': str(user.phone_number),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'role': user.role,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'mfa_enabled': user.mfa_enabled
        })

    return Response({
        'count': queryset.count(),
        'results': users_data
    })


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_user_detail(request, user_id):
    """Get, update, or delete a specific user."""

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Get user details
        data = {
            'id': user.id,
            'phone_number': str(user.phone_number),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'is_active': user.is_active,
            'is_verified': user.is_verified,
            'is_staff': user.is_staff,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
            'mfa_enabled': user.mfa_enabled
        }

        # Add profile data if exists
        if hasattr(user, 'profile'):
            data['profile'] = {
                'country': user.profile.country,
                'city': user.profile.city,
                'preferred_language': user.profile.preferred_language,
                'preferred_currency': user.profile.preferred_currency
            }

        return Response(data)

    elif request.method == 'PUT':
        # Update user
        user.is_active = request.data.get('is_active', user.is_active)
        user.is_verified = request.data.get('is_verified', user.is_verified)
        user.role = request.data.get('role', user.role)
        user.save()

        return Response({'message': 'User updated successfully'})

    elif request.method == 'DELETE':
        # Prevent self-deletion
        if user.id == request.user.id:
            return Response(
                {'error': 'Cannot delete your own account'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()
        return Response({'message': 'User deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_products_list(request):
    """List all products for admin moderation."""

    # Get query parameters
    category = request.query_params.get('category')
    is_active = request.query_params.get('is_active')
    is_featured = request.query_params.get('is_featured')
    search = request.query_params.get('search')

    # Base queryset
    queryset = Product.objects.all().select_related('seller', 'category')

    # Apply filters
    if category:
        queryset = queryset.filter(category_id=category)
    if is_active is not None:
        queryset = queryset.filter(is_active=is_active.lower() == 'true')
    if is_featured is not None:
        queryset = queryset.filter(is_featured=is_featured.lower() == 'true')
    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )

    # Serialize data
    products_data = []
    for product in queryset[:100]:  # Limit for performance
        products_data.append({
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'seller_name': product.seller.get_full_name(),
            'seller_id': product.seller.id,
            'category_name': product.category.get_name_display() if product.category else None,
            'price': str(product.price),
            'stock_quantity': product.stock_quantity,
            'availability': product.availability,
            'is_active': product.is_active,
            'is_featured': product.is_featured,
            'views_count': product.views_count,
            'sales_count': product.sales_count,
            'created_at': product.created_at
        })

    return Response({
        'count': queryset.count(),
        'results': products_data
    })


@api_view(['PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def admin_product_action(request, product_id):
    """Update or delete a product (admin moderation)."""

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Update product status
        product.is_active = request.data.get('is_active', product.is_active)
        product.is_featured = request.data.get('is_featured', product.is_featured)
        product.save()

        return Response({'message': 'Product updated successfully'})

    elif request.method == 'DELETE':
        product.delete()
        return Response({'message': 'Product deleted successfully'})


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_orders_list(request):
    """List all orders for admin."""

    # Get query parameters
    status_filter = request.query_params.get('status')
    search = request.query_params.get('search')

    # Base queryset
    queryset = Order.objects.all().select_related('buyer', 'seller')

    # Apply filters
    if status_filter:
        queryset = queryset.filter(status=status_filter)
    if search:
        queryset = queryset.filter(
            Q(tracking_number__icontains=search) |
            Q(buyer__first_name__icontains=search) |
            Q(buyer__last_name__icontains=search) |
            Q(seller__first_name__icontains=search) |
            Q(seller__last_name__icontains=search)
        )

    # Serialize data
    orders_data = []
    for order in queryset[:100]:  # Limit for performance
        orders_data.append({
            'id': order.id,
            'tracking_number': order.tracking_number,
            'buyer_name': order.buyer.get_full_name(),
            'buyer_id': order.buyer.id,
            'seller_name': order.seller.get_full_name(),
            'seller_id': order.seller.id,
            'status': order.status,
            'payment_status': order.payment_status,
            'payment_method': order.payment_method,
            'total_amount': str(order.total_amount),
            'currency': order.currency,
            'items_count': order.items.count(),
            'created_at': order.created_at
        })

    return Response({
        'count': queryset.count(),
        'results': orders_data
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_subscriptions_list(request):
    """List all subscriptions."""

    status_filter = request.query_params.get('status')

    queryset = Subscription.objects.all().select_related('user')

    if status_filter:
        queryset = queryset.filter(status=status_filter)

    subscriptions_data = []
    for sub in queryset[:100]:
        subscriptions_data.append({
            'id': sub.id,
            'user_name': sub.user.get_full_name(),
            'user_id': sub.user.id,
            'plan': sub.plan,
            'status': sub.status,
            'start_date': sub.start_date,
            'end_date': sub.end_date,
            'price': str(sub.price),
            'currency': sub.currency,
            'days_remaining': sub.days_remaining()
        })

    return Response({
        'count': queryset.count(),
        'results': subscriptions_data
    })
