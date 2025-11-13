"""
URL configuration for products app.
"""
from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    ProductDetailView,
    SellerProductListView,
    SellerProductDetailView,
    ProductImageUploadView,
    ProductImageDeleteView,
    SavedProductListView,
    SavedProductDeleteView,
    toggle_saved_product,
    featured_products,
    popular_products,
)

app_name = 'products'

urlpatterns = [
    # Categories
    path('categories/', CategoryListView.as_view(), name='category_list'),

    # Public product endpoints
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('featured/', featured_products, name='featured_products'),
    path('popular/', popular_products, name='popular_products'),

    # Seller product management
    path('seller/products/', SellerProductListView.as_view(), name='seller_product_list'),
    path('seller/products/<int:pk>/', SellerProductDetailView.as_view(), name='seller_product_detail'),

    # Product images
    path('images/upload/', ProductImageUploadView.as_view(), name='product_image_upload'),
    path('images/<int:pk>/delete/', ProductImageDeleteView.as_view(), name='product_image_delete'),

    # Saved/Favorite products
    path('saved/', SavedProductListView.as_view(), name='saved_product_list'),
    path('saved/<int:pk>/delete/', SavedProductDeleteView.as_view(), name='saved_product_delete'),
    path('<int:product_id>/toggle-save/', toggle_saved_product, name='toggle_saved_product'),
]
