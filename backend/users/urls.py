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
]
