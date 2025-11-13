"""
Views for subscription management.
"""
from rest_framework import generics, permissions
from .models import Subscription
from .serializers import SubscriptionSerializer


class SubscriptionListView(generics.ListAPIView):
    """List user subscriptions."""

    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscriptionCreateView(generics.CreateAPIView):
    """Create a new subscription."""

    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
