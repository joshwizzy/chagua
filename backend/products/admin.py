"""
Admin configuration for products app.
"""
from django.contrib import admin
from .models import Category, Product, ProductImage, ProductAttribute, ProductVariant, SavedProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ['name', 'slug', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images."""

    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'order']


class ProductVariantInline(admin.TabularInline):
    """Inline admin for product variants."""

    model = ProductVariant
    extra = 1
    fields = ['attribute', 'value', 'price_adjustment', 'stock_quantity', 'sku']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""

    list_display = ['name', 'seller', 'category', 'price', 'availability', 'stock_quantity',
                    'is_active', 'is_featured', 'views_count', 'sales_count', 'created_at']
    list_filter = ['category', 'availability', 'is_active', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'seller__phone_number', 'seller__first_name', 'seller__last_name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ['views_count', 'sales_count', 'created_at', 'updated_at']


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin interface for ProductAttribute model."""

    list_display = ['name']
    search_fields = ['name']


@admin.register(SavedProduct)
class SavedProductAdmin(admin.ModelAdmin):
    """Admin interface for SavedProduct model."""

    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__phone_number', 'user__first_name', 'product__name']
