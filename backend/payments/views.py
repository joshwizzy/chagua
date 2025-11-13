"""
Views for payment processing.
"""
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer


class PaymentInitiateView(generics.CreateAPIView):
    """Initiate a payment."""

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PaymentDetailView(generics.RetrieveAPIView):
    """Get payment details."""

    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
