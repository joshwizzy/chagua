"""
Serializers for user authentication and profile management.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User, UserProfile, DeliveryAddress


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    pin = serializers.CharField(write_only=True, min_length=4, max_length=6)
    pin_confirm = serializers.CharField(write_only=True, min_length=4, max_length=6)

    class Meta:
        model = User
        fields = ['phone_number', 'email', 'first_name', 'last_name', 'role', 'pin', 'pin_confirm']

    def validate(self, attrs):
        if attrs['pin'] != attrs['pin_confirm']:
            raise serializers.ValidationError({"pin": "PINs do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('pin_confirm')
        pin = validated_data.pop('pin')
        user = User.objects.create_user(pin=pin, **validated_data)

        # Create user profile
        UserProfile.objects.create(user=user)

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""

    phone_number = PhoneNumberField()
    pin = serializers.CharField(write_only=True)
    mfa_token = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        pin = attrs.get('pin')
        mfa_token = attrs.get('mfa_token')

        user = authenticate(username=phone_number, password=pin)

        if not user:
            raise serializers.ValidationError("Invalid phone number or PIN.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Check MFA if enabled
        if user.mfa_enabled:
            if not mfa_token:
                raise serializers.ValidationError({"mfa_token": "MFA token is required."})
            if not user.verify_mfa_token(mfa_token):
                raise serializers.ValidationError({"mfa_token": "Invalid MFA token."})

        attrs['user'] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'country', 'city', 'address', 'preferred_language',
                  'preferred_currency', 'email_notifications', 'sms_notifications']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details."""

    profile = UserProfileSerializer(read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'email', 'first_name', 'last_name', 'full_name',
                  'role', 'mfa_enabled', 'is_verified', 'date_joined', 'profile']
        read_only_fields = ['id', 'phone_number', 'role', 'date_joined']


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password/PIN."""

    old_pin = serializers.CharField(required=True)
    new_pin = serializers.CharField(required=True, min_length=4, max_length=6)
    new_pin_confirm = serializers.CharField(required=True, min_length=4, max_length=6)

    def validate(self, attrs):
        if attrs['new_pin'] != attrs['new_pin_confirm']:
            raise serializers.ValidationError({"new_pin": "New PINs do not match."})
        return attrs


class MFASetupSerializer(serializers.Serializer):
    """Serializer for MFA setup."""

    action = serializers.ChoiceField(choices=['enable', 'disable'])
    token = serializers.CharField(required=False)

    def validate(self, attrs):
        action = attrs.get('action')
        token = attrs.get('token')

        if action == 'enable' and not token:
            raise serializers.ValidationError({"token": "Token is required to enable MFA."})

        return attrs


class DeliveryAddressSerializer(serializers.ModelSerializer):
    """Serializer for delivery addresses."""

    class Meta:
        model = DeliveryAddress
        fields = ['id', 'label', 'recipient_name', 'phone_number', 'country', 'city',
                  'address_line1', 'address_line2', 'postal_code', 'is_default',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
