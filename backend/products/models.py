"""
Product models for CHAGUA E-Commerce Platform.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from users.models import User


class Category(models.Model):
    """Product categories."""

    CATEGORY_CHOICES = [
        ('CLOTHES', 'Clothes'),
        ('COSMETICS', 'Cosmetics'),
        ('SHOES', 'Shoes'),
        ('JEWELRY', 'Jewelry'),
        ('BAGS', 'Bags'),
        ('GADGETS', 'Gadgets'),
        ('OTHERS', 'Others'),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True, verbose_name=_('Category Name'))
    slug = models.SlugField(max_length=50, unique=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))
    icon = models.ImageField(upload_to='categories/', blank=True, null=True, verbose_name=_('Icon'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class Product(models.Model):
    """Product listings."""

    AVAILABILITY_CHOICES = [
        ('IN_STOCK', 'In Stock'),
        ('OUT_OF_STOCK', 'Out of Stock'),
        ('PRE_ORDER', 'Pre-order'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', verbose_name=_('Seller'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name=_('Category'))

    name = models.CharField(max_length=255, verbose_name=_('Product Name'))
    slug = models.SlugField(max_length=255, unique=True, verbose_name=_('Slug'))
    description = models.TextField(verbose_name=_('Description'))
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_('Price'))

    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='IN_STOCK', verbose_name=_('Availability'))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_('Stock Quantity'))

    # SEO and metadata
    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Meta Title'))
    meta_description = models.TextField(blank=True, null=True, verbose_name=_('Meta Description'))

    # Status
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_featured = models.BooleanField(default=False, verbose_name=_('Featured'))

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Analytics
    views_count = models.PositiveIntegerField(default=0, verbose_name=_('Views Count'))
    sales_count = models.PositiveIntegerField(default=0, verbose_name=_('Sales Count'))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['seller', 'is_active']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name

    def increment_views(self):
        """Increment product views count."""
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_sales(self):
        """Increment product sales count."""
        self.sales_count += 1
        self.save(update_fields=['sales_count'])

    def reduce_stock(self, quantity):
        """Reduce stock quantity."""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            if self.stock_quantity == 0:
                self.availability = 'OUT_OF_STOCK'
            self.save(update_fields=['stock_quantity', 'availability'])
            return True
        return False

    @property
    def average_rating(self):
        """Calculate average rating for the product."""
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return reviews.aggregate(models.Avg('rating'))['rating__avg']
        return 0


class ProductImage(models.Model):
    """Product images."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_('Product'))
    image = models.ImageField(upload_to='products/', verbose_name=_('Image'))
    alt_text = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Alt Text'))
    is_primary = models.BooleanField(default=False, verbose_name=_('Primary Image'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Order'))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')
        ordering = ['order', '-is_primary', 'created_at']

    def __str__(self):
        return f"Image for {self.product.name}"

    def save(self, *args, **kwargs):
        # If this is the primary image, unset all other primary images for this product
        if self.is_primary:
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    """Product attributes (e.g., Size, Color)."""

    name = models.CharField(max_length=50, verbose_name=_('Attribute Name'))

    class Meta:
        verbose_name = _('Product Attribute')
        verbose_name_plural = _('Product Attributes')

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    """Product variants with different attributes."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name=_('Product'))
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, verbose_name=_('Attribute'))
    value = models.CharField(max_length=100, verbose_name=_('Value'))
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('Price Adjustment'))
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name=_('Stock Quantity'))
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, verbose_name=_('SKU'))

    class Meta:
        verbose_name = _('Product Variant')
        verbose_name_plural = _('Product Variants')
        unique_together = ['product', 'attribute', 'value']

    def __str__(self):
        return f"{self.product.name} - {self.attribute.name}: {self.value}"


class SavedProduct(models.Model):
    """User's saved/favorite products."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_products', verbose_name=_('User'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='saved_by', verbose_name=_('Product'))

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Saved Product')
        verbose_name_plural = _('Saved Products')
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} saved {self.product.name}"
