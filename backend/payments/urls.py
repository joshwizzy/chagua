"""
URL configuration for payments app.
"""
from django.urls import path
from .views import PaymentInitiateView, PaymentDetailView

app_name = 'payments'

urlpatterns = [
    path('initiate/', PaymentInitiateView.as_view(), name='payment_initiate'),
    path('<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]
