# notifications/urls.py
from django.urls import path
from .views import NotificationListAPIView, MarkNotificationReadAPIView

urlpatterns = [
    path('', NotificationListAPIView.as_view(), name='notifications-list'),
    path('mark-read/<int:pk>/', MarkNotificationReadAPIView.as_view(), name='notification-mark-read'),
]
