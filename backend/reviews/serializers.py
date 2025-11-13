"""
Serializers for reviews and ratings.
"""
from rest_framework import serializers
from .models import ProductReview, SellerReview


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews."""

    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'user_name', 'rating', 'title', 'comment', 'photo', 'created_at']
        read_only_fields = ['id', 'user_name', 'created_at']


class SellerReviewSerializer(serializers.ModelSerializer):
    """Serializer for seller reviews."""

    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = SellerReview
        fields = ['id', 'seller', 'reviewer_name', 'reliability_rating', 'communication_rating',
                  'delivery_speed_rating', 'average_rating', 'comment', 'created_at']
        read_only_fields = ['id', 'reviewer_name', 'average_rating', 'created_at']
