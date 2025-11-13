"""
URL configuration for notifications app.
"""
from django.urls import path
from .views import NotificationListView, mark_as_read

app_name = 'notifications'

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('<int:pk>/read/', mark_as_read, name='mark_as_read'),
]
