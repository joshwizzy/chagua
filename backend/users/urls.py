"""
URL configuration for users app.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView,
    UserProfileDetailView,
    ChangePasswordView,
    MFASetupView,
    DeliveryAddressListCreateView,
    DeliveryAddressDetailView,
    logout_view
)
from .admin_views import (
    admin_statistics,
    admin_users_list,
    admin_user_detail,
    admin_products_list,
    admin_product_action,
    admin_orders_list,
    admin_subscriptions_list
)

app_name = 'users'

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/details/', UserProfileDetailView.as_view(), name='profile_detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # MFA
    path('mfa/', MFASetupView.as_view(), name='mfa_setup'),

    # Delivery Addresses
    path('addresses/', DeliveryAddressListCreateView.as_view(), name='address_list'),
    path('addresses/<int:pk>/', DeliveryAddressDetailView.as_view(), name='address_detail'),

    # Admin endpoints
    path('admin/statistics/', admin_statistics, name='admin_statistics'),
    path('admin/users/', admin_users_list, name='admin_users_list'),
    path('admin/users/<int:user_id>/', admin_user_detail, name='admin_user_detail'),
    path('admin/products/', admin_products_list, name='admin_products_list'),
    path('admin/products/<int:product_id>/', admin_product_action, name='admin_product_action'),
    path('admin/orders/', admin_orders_list, name='admin_orders_list'),
    path('admin/subscriptions/', admin_subscriptions_list, name='admin_subscriptions_list'),
]
