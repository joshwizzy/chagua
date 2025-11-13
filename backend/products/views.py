"""
Views for product management.
"""
from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product, ProductImage, SavedProduct
from .serializers import (
    CategorySerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer,
    SavedProductSerializer
)
from .permissions import IsSellerOrReadOnly


class CategoryListView(generics.ListAPIView):
    """API endpoint for listing all categories."""

    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    """API endpoint for listing products with filtering and search."""

    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'availability', 'is_featured']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'views_count', 'sales_count']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related('category', 'seller')

        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')

        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """API endpoint for viewing product details."""

    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment views count
        instance.increment_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SellerProductListView(generics.ListCreateAPIView):
    """API endpoint for sellers to list their products and create new ones."""

    permission_classes = [permissions.IsAuthenticated, IsSellerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at', 'views_count', 'sales_count']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).select_related('category')


class SellerProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for sellers to manage their product details."""

    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated, IsSellerOrReadOnly]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class ProductImageUploadView(generics.CreateAPIView):
    """API endpoint for uploading product images."""

    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsSellerOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        try:
            product = Product.objects.get(id=product_id, seller=self.request.user)
            serializer.save(product=product)
        except Product.DoesNotExist:
            raise permissions.PermissionDenied("You don't have permission to add images to this product.")


class ProductImageDeleteView(generics.DestroyAPIView):
    """API endpoint for deleting product images."""

    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticated, IsSellerOrReadOnly]

    def get_queryset(self):
        return ProductImage.objects.filter(product__seller=self.request.user)


class SavedProductListView(generics.ListCreateAPIView):
    """API endpoint for managing saved/favorite products."""

    serializer_class = SavedProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedProduct.objects.filter(user=self.request.user).select_related('product')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedProductDeleteView(generics.DestroyAPIView):
    """API endpoint for removing saved products."""

    serializer_class = SavedProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedProduct.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_saved_product(request, product_id):
    """Toggle saved/favorite status for a product."""
    try:
        product = Product.objects.get(id=product_id, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {'error': 'Product not found.'},
            status=status.HTTP_404_NOT_FOUND
        )

    saved_product, created = SavedProduct.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        saved_product.delete()
        return Response(
            {'message': 'Product removed from favorites.', 'is_saved': False},
            status=status.HTTP_200_OK
        )

    return Response(
        {'message': 'Product added to favorites.', 'is_saved': True},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_products(request):
    """Get featured products."""
    products = Product.objects.filter(is_active=True, is_featured=True).select_related('category', 'seller')[:10]
    serializer = ProductListSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_products(request):
    """Get popular products based on sales count."""
    products = Product.objects.filter(is_active=True).order_by('-sales_count').select_related('category', 'seller')[:10]
    serializer = ProductListSerializer(products, many=True, context={'request': request})
    return Response(serializer.data)
