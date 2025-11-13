"""
Payment gateway integration services.
"""
from django.conf import settings
import requests
import hashlib
import time


class MobileMoneyService:
    """Mobile Money payment processing."""

    @staticmethod
    def initiate_payment(phone_number, amount, currency, reference):
        """
        Initiate a mobile money payment.

        Args:
            phone_number: Customer's phone number
            amount: Amount to charge
            currency: Currency code (UGX, RWF, BIF)
            reference: Unique reference for this transaction

        Returns:
            dict: Payment response with status and transaction_id
        """
        # This is a template implementation
        # Replace with actual mobile money API integration (MTN, Airtel, etc.)

        if not settings.MOBILE_MONEY_API_KEY:
            # Development mode - simulate successful payment
            return {
                'success': True,
                'transaction_id': f'SIM{int(time.time())}',
                'status': 'PENDING',
                'message': 'Payment initiated (simulated)'
            }

        # Production implementation would call actual API
        # Example for MTN Mobile Money:
        try:
            api_url = settings.MOBILE_MONEY_API_URL if hasattr(settings, 'MOBILE_MONEY_API_URL') else ''
            headers = {
                'Authorization': f'Bearer {settings.MOBILE_MONEY_API_KEY}',
                'Content-Type': 'application/json'
            }

            payload = {
                'phone_number': phone_number,
                'amount': float(amount),
                'currency': currency,
                'reference': reference,
                'callback_url': f'{settings.SITE_URL}/api/payments/callback/' if hasattr(settings, 'SITE_URL') else ''
            }

            response = requests.post(
                f'{api_url}/payments/request',
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'transaction_id': data.get('transaction_id'),
                    'status': data.get('status', 'PENDING'),
                    'message': 'Payment initiated successfully'
                }
            else:
                return {
                    'success': False,
                    'error': 'Payment initiation failed',
                    'message': response.text
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to connect to payment gateway'
            }

    @staticmethod
    def check_payment_status(transaction_id):
        """
        Check the status of a payment transaction.

        Args:
            transaction_id: The transaction ID to check

        Returns:
            dict: Payment status information
        """
        if not settings.MOBILE_MONEY_API_KEY:
            # Development mode
            return {
                'status': 'COMPLETED',
                'transaction_id': transaction_id
            }

        try:
            api_url = settings.MOBILE_MONEY_API_URL if hasattr(settings, 'MOBILE_MONEY_API_URL') else ''
            headers = {
                'Authorization': f'Bearer {settings.MOBILE_MONEY_API_KEY}',
                'Content-Type': 'application/json'
            }

            response = requests.get(
                f'{api_url}/payments/{transaction_id}/status',
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    'status': 'UNKNOWN',
                    'error': 'Failed to check status'
                }

        except Exception as e:
            return {
                'status': 'ERROR',
                'error': str(e)
            }

    @staticmethod
    def process_callback(callback_data):
        """
        Process payment callback from mobile money provider.

        Args:
            callback_data: Callback data from payment provider

        Returns:
            dict: Processed callback information
        """
        # Verify callback signature/hash if required
        # Update payment status in database
        # Send notifications

        return {
            'success': True,
            'transaction_id': callback_data.get('transaction_id'),
            'status': callback_data.get('status')
        }


class AirtelMoneyService(MobileMoneyService):
    """Airtel Money specific implementation."""
    pass


class MTNMoneyService(MobileMoneyService):
    """MTN Mobile Money specific implementation."""
    pass
