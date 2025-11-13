from django.contrib import admin
from .models import ProductReview, SellerReview


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved', 'created_at']
    search_fields = ['product__name', 'user__phone_number', 'title', 'comment']


@admin.register(SellerReview)
class SellerReviewAdmin(admin.ModelAdmin):
    list_display = ['seller', 'reviewer', 'reliability_rating', 'communication_rating',
                    'delivery_speed_rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['seller__phone_number', 'reviewer__phone_number', 'comment']
