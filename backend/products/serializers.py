"""
Serializers for product management.
"""
from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductAttribute, ProductVariant, SavedProduct


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images."""

    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'alt_text', 'is_primary', 'order', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for product variants."""

    attribute_name = serializers.CharField(source='attribute.name', read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'attribute', 'attribute_name', 'value', 'price_adjustment', 'stock_quantity', 'sku']
        read_only_fields = ['id']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product listing (summary view)."""

    category_name = serializers.CharField(source='category.get_name_display', read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'availability', 'stock_quantity',
                  'category_name', 'seller_name', 'primary_image', 'is_featured', 'average_rating',
                  'views_count', 'sales_count', 'created_at']
        read_only_fields = ['id', 'slug', 'views_count', 'sales_count', 'created_at']

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return self.context['request'].build_absolute_uri(primary_image.image.url)
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product detail view."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)
    seller_phone = serializers.CharField(source='seller.phone_number', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'availability', 'stock_quantity',
                  'category', 'category_id', 'seller_name', 'seller_phone', 'images', 'variants',
                  'meta_title', 'meta_description', 'is_active', 'is_featured', 'average_rating',
                  'views_count', 'sales_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'seller_name', 'seller_phone', 'views_count', 'sales_count',
                            'created_at', 'updated_at']

    def create(self, validated_data):
        # Automatically set the seller to the authenticated user
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating products."""

    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'availability', 'stock_quantity',
                  'category', 'meta_title', 'meta_description', 'is_active', 'is_featured', 'images']
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)


class SavedProductSerializer(serializers.ModelSerializer):
    """Serializer for saved products."""

    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = SavedProduct
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'created_at']
