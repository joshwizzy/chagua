"""
Notification services for SMS, Email, and WhatsApp.
"""
from django.conf import settings
from twilio.rest import Client
from django.core.mail import send_mail
import requests


class SMSService:
    """Send SMS notifications using Twilio."""

    @staticmethod
    def send_sms(to_number, message):
        """Send an SMS message."""
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            print(f"SMS not configured. Would send to {to_number}: {message}")
            return False

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=str(to_number)
            )
            return True
        except Exception as e:
            print(f"Failed to send SMS: {e}")
            return False


class EmailService:
    """Send email notifications."""

    @staticmethod
    def send_email(to_email, subject, message):
        """Send an email."""
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@chagua.com',
                recipient_list=[to_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


class WhatsAppService:
    """Send WhatsApp notifications using Twilio WhatsApp API."""

    @staticmethod
    def send_whatsapp(to_number, message):
        """Send a WhatsApp message."""
        if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
            print(f"WhatsApp not configured. Would send to {to_number}: {message}")
            return False

        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                body=message,
                from_=f'whatsapp:{settings.TWILIO_PHONE_NUMBER}',
                to=f'whatsapp:{to_number}'
            )
            return True
        except Exception as e:
            print(f"Failed to send WhatsApp: {e}")
            return False


class NotificationService:
    """Main notification service to send multi-channel notifications."""

    @staticmethod
    def notify_order_created(order):
        """Notify buyer and seller when order is created."""
        # Notify buyer
        buyer_message = f"Your order #{order.tracking_number} has been placed successfully. Total: {order.total_amount} {order.currency}"
        SMSService.send_sms(order.buyer.phone_number, buyer_message)

        if order.buyer.email:
            EmailService.send_email(
                order.buyer.email,
                f"Order Confirmation - #{order.tracking_number}",
                buyer_message
            )

        # Notify seller
        seller_message = f"New order #{order.tracking_number} from {order.buyer.get_full_name()}. Total: {order.total_amount} {order.currency}. Check your dashboard for details."
        SMSService.send_sms(order.seller.phone_number, seller_message)
        WhatsAppService.send_whatsapp(order.seller.phone_number, seller_message)

        if order.seller.email:
            EmailService.send_email(
                order.seller.email,
                f"New Order - #{order.tracking_number}",
                seller_message
            )

    @staticmethod
    def notify_order_status_changed(order, old_status, new_status):
        """Notify relevant parties when order status changes."""
        status_messages = {
            'CONFIRMED': f"Your order #{order.tracking_number} has been confirmed by the seller.",
            'SHIPPED': f"Your order #{order.tracking_number} has been shipped! Track it with this number.",
            'DELIVERED': f"Your order #{order.tracking_number} has been delivered. Thank you for shopping with CHAGUA!",
            'CANCELLED': f"Your order #{order.tracking_number} has been cancelled."
        }

        if new_status in status_messages:
            message = status_messages[new_status]
            SMSService.send_sms(order.buyer.phone_number, message)

            if order.buyer.email:
                EmailService.send_email(
                    order.buyer.email,
                    f"Order Update - #{order.tracking_number}",
                    message
                )

    @staticmethod
    def notify_subscription_expiring(user, days_remaining):
        """Notify seller about expiring subscription."""
        message = f"Your CHAGUA subscription will expire in {days_remaining} days. Renew now to keep your products listed."
        SMSService.send_sms(user.phone_number, message)

        if user.email:
            EmailService.send_email(
                user.email,
                "Subscription Expiring Soon",
                message
            )
