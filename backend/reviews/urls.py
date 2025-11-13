"""
URL configuration for reviews app.
"""
from django.urls import path
from .views import ProductReviewListView, SellerReviewListView

app_name = 'reviews'

urlpatterns = [
    path('products/<int:product_id>/', ProductReviewListView.as_view(), name='product_review_list'),
    path('sellers/<int:seller_id>/', SellerReviewListView.as_view(), name='seller_review_list'),
]
