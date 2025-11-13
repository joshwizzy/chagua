"""
URL configuration for orders app.
"""
from django.urls import path
from .views import (
    OrderListView,
    BuyerOrderListView,
    SellerOrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderStatusUpdateView,
    OrderCancelView,
    CartView,
    AddToCartView,
    UpdateCartItemView,
    RemoveFromCartView,
    ClearCartView,
    OrderStatusHistoryView,
    track_order,
)

app_name = 'orders'

urlpatterns = [
    # Orders
    path('', OrderListView.as_view(), name='order_list'),
    path('buyer/', BuyerOrderListView.as_view(), name='buyer_order_list'),
    path('seller/', SellerOrderListView.as_view(), name='seller_order_list'),
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('<str:tracking_number>/', OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('<int:pk>/cancel/', OrderCancelView.as_view(), name='order_cancel'),
    path('<str:tracking_number>/history/', OrderStatusHistoryView.as_view(), name='order_history'),
    path('track/<str:tracking_number>/', track_order, name='track_order'),

    # Cart
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/items/<int:pk>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('cart/items/<int:pk>/remove/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('cart/clear/', ClearCartView.as_view(), name='clear_cart'),
]
