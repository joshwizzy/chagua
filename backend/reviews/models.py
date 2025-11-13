"""
Review models for CHAGUA E-Commerce Platform.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from products.models import Product


class ProductReview(models.Model):
    """Product reviews and ratings."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('Product'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name=_('User'))

    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Rating')
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    comment = models.TextField(verbose_name=_('Comment'))

    # Optional photo
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name=_('Photo'))

    # Moderation
    is_approved = models.BooleanField(default=True, verbose_name=_('Approved'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product Review')
        verbose_name_plural = _('Product Reviews')
        ordering = ['-created_at']
        unique_together = ['product', 'user']

    def __str__(self):
        return f"{self.user} - {self.product.name} ({self.rating}/5)"


class SellerReview(models.Model):
    """Seller ratings and reviews."""

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_reviews', verbose_name=_('Seller'))
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_seller_reviews', verbose_name=_('Reviewer'))

    reliability_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Reliability Rating')
    )
    communication_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Communication Rating')
    )
    delivery_speed_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Delivery Speed Rating')
    )

    comment = models.TextField(blank=True, null=True, verbose_name=_('Comment'))
    is_approved = models.BooleanField(default=True, verbose_name=_('Approved'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Seller Review')
        verbose_name_plural = _('Seller Reviews')
        ordering = ['-created_at']
        unique_together = ['seller', 'reviewer']

    def __str__(self):
        return f"{self.reviewer} reviewed {self.seller}"

    @property
    def average_rating(self):
        return (self.reliability_rating + self.communication_rating + self.delivery_speed_rating) / 3
