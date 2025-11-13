"""
User models for CHAGUA E-Commerce Platform.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
import pyotp
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for phone-based authentication."""

    def create_user(self, phone_number, pin, **extra_fields):
        """Create and save a regular user with the given phone number and PIN."""
        if not phone_number:
            raise ValueError(_('The phone number must be set'))
        if not pin:
            raise ValueError(_('The PIN must be set'))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(pin)  # PIN is stored as hashed password
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, pin, **extra_fields):
        """Create and save a superuser with the given phone number and PIN."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'ADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(phone_number, pin, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User model with phone number and PIN authentication."""

    ROLE_CHOICES = [
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
        ('ADMIN', 'Administrator'),
    ]

    phone_number = PhoneNumberField(unique=True, verbose_name=_('Phone Number'))
    email = models.EmailField(blank=True, null=True, verbose_name=_('Email'))
    first_name = models.CharField(max_length=150, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=150, verbose_name=_('Last Name'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='BUYER', verbose_name=_('Role'))

    # MFA fields
    mfa_enabled = models.BooleanField(default=False, verbose_name=_('MFA Enabled'))
    mfa_secret = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('MFA Secret'))

    # Account status
    is_active = models.BooleanField(default=True, verbose_name=_('Active'))
    is_staff = models.BooleanField(default=False, verbose_name=_('Staff Status'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Phone Verified'))

    # Timestamps
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_('Date Joined'))
    last_login = models.DateTimeField(blank=True, null=True, verbose_name=_('Last Login'))

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']

    def __str__(self):
        return str(self.phone_number)

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def enable_mfa(self):
        """Enable MFA for the user and generate a secret."""
        if not self.mfa_secret:
            self.mfa_secret = pyotp.random_base32()
        self.mfa_enabled = True
        self.save()
        return self.mfa_secret

    def disable_mfa(self):
        """Disable MFA for the user."""
        self.mfa_enabled = False
        self.save()

    def verify_mfa_token(self, token):
        """Verify the MFA token."""
        if not self.mfa_enabled or not self.mfa_secret:
            return False
        totp = pyotp.TOTP(self.mfa_secret)
        return totp.verify(token, valid_window=1)

    def get_mfa_qr_code_uri(self):
        """Get the MFA QR code URI for setup."""
        if not self.mfa_secret:
            self.enable_mfa()
        return pyotp.totp.TOTP(self.mfa_secret).provisioning_uri(
            name=str(self.phone_number),
            issuer_name='CHAGUA'
        )


class UserProfile(models.Model):
    """Extended profile information for users."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name=_('Avatar'))
    bio = models.TextField(blank=True, null=True, verbose_name=_('Bio'))

    # Location
    country = models.CharField(max_length=2, choices=[
        ('UG', 'Uganda'),
        ('RW', 'Rwanda'),
        ('BI', 'Burundi'),
    ], default='UG', verbose_name=_('Country'))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('City'))
    address = models.TextField(blank=True, null=True, verbose_name=_('Address'))

    # Preferences
    preferred_language = models.CharField(max_length=2, choices=[
        ('en', 'English'),
        ('fr', 'French'),
        ('sw', 'Swahili'),
    ], default='en', verbose_name=_('Preferred Language'))
    preferred_currency = models.CharField(max_length=3, choices=[
        ('UGX', 'Ugandan Shilling'),
        ('RWF', 'Rwandan Franc'),
        ('BIF', 'Burundian Franc'),
    ], default='UGX', verbose_name=_('Preferred Currency'))

    # Notifications preferences
    email_notifications = models.BooleanField(default=True, verbose_name=_('Email Notifications'))
    sms_notifications = models.BooleanField(default=True, verbose_name=_('SMS Notifications'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"


class DeliveryAddress(models.Model):
    """Delivery addresses for users."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='delivery_addresses')
    label = models.CharField(max_length=50, verbose_name=_('Label'), help_text=_('e.g., Home, Office'))
    recipient_name = models.CharField(max_length=200, verbose_name=_('Recipient Name'))
    phone_number = PhoneNumberField(verbose_name=_('Phone Number'))
    country = models.CharField(max_length=2, choices=[
        ('UG', 'Uganda'),
        ('RW', 'Rwanda'),
        ('BI', 'Burundi'),
    ], verbose_name=_('Country'))
    city = models.CharField(max_length=100, verbose_name=_('City'))
    address_line1 = models.CharField(max_length=255, verbose_name=_('Address Line 1'))
    address_line2 = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Address Line 2'))
    postal_code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Postal Code'))
    is_default = models.BooleanField(default=False, verbose_name=_('Default Address'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Delivery Address')
        verbose_name_plural = _('Delivery Addresses')
        ordering = ['-is_default', '-created_at']

    def __str__(self):
        return f"{self.label} - {self.recipient_name}"

    def save(self, *args, **kwargs):
        # If this is the default address, unset all other default addresses for this user
        if self.is_default:
            DeliveryAddress.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)
