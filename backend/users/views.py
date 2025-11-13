"""
Views for user authentication and profile management.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import update_session_auth_hash
from .models import User, UserProfile, DeliveryAddress
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer,
    MFASetupSerializer,
    DeliveryAddressSerializer
)
import qrcode
import io
import base64


class UserRegistrationView(APIView):
    """API endpoint for user registration."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """API endpoint for user login."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint for viewing and updating user profile."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """API endpoint for viewing and updating extended user profile."""

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class ChangePasswordView(APIView):
    """API endpoint for changing user password/PIN."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user

            # Check old PIN
            if not user.check_password(serializer.data.get('old_pin')):
                return Response(
                    {'old_pin': 'Wrong PIN.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Set new PIN
            user.set_password(serializer.data.get('new_pin'))
            user.save()
            update_session_auth_hash(request, user)

            return Response(
                {'message': 'PIN changed successfully.'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MFASetupView(APIView):
    """API endpoint for MFA setup and management."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get MFA QR code for setup."""
        user = request.user

        if not user.mfa_secret:
            user.enable_mfa()

        # Generate QR code
        qr_uri = user.get_mfa_qr_code_uri()
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_uri)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()

        return Response({
            'qr_code': f'data:image/png;base64,{img_str}',
            'secret': user.mfa_secret,
            'uri': qr_uri
        })

    def post(self, request):
        """Enable or disable MFA."""
        serializer = MFASetupSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            action = serializer.validated_data['action']

            if action == 'enable':
                token = serializer.validated_data.get('token')
                if not user.mfa_secret:
                    user.enable_mfa()

                if user.verify_mfa_token(token):
                    user.mfa_enabled = True
                    user.save()
                    return Response(
                        {'message': 'MFA enabled successfully.'},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'token': 'Invalid token.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            elif action == 'disable':
                user.disable_mfa()
                return Response(
                    {'message': 'MFA disabled successfully.'},
                    status=status.HTTP_200_OK
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    """API endpoint for listing and creating delivery addresses."""

    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating, and deleting delivery addresses."""

    serializer_class = DeliveryAddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """API endpoint for user logout."""
    try:
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
