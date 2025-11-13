"""
URL configuration for subscriptions app.
"""
from django.urls import path
from .views import SubscriptionListView, SubscriptionCreateView

app_name = 'subscriptions'

urlpatterns = [
    path('', SubscriptionListView.as_view(), name='subscription_list'),
    path('create/', SubscriptionCreateView.as_view(), name='subscription_create'),
]
