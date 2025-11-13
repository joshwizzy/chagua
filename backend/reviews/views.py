"""
Views for reviews and ratings.
"""
from rest_framework import generics, permissions
from .models import ProductReview, SellerReview
from .serializers import ProductReviewSerializer, SellerReviewSerializer


class ProductReviewListView(generics.ListCreateAPIView):
    """List and create product reviews."""

    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(product_id=product_id, is_approved=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SellerReviewListView(generics.ListCreateAPIView):
    """List and create seller reviews."""

    serializer_class = SellerReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        seller_id = self.kwargs.get('seller_id')
        return SellerReview.objects.filter(seller_id=seller_id, is_approved=True)

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)
