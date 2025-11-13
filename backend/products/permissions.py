"""
Custom permissions for products app.
"""
from rest_framework import permissions


class IsSellerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow sellers to create/edit products.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to authenticated sellers
        return request.user and request.user.is_authenticated and request.user.role in ['SELLER', 'ADMIN']

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the seller who owns the product
        return obj.seller == request.user or request.user.role == 'ADMIN'
