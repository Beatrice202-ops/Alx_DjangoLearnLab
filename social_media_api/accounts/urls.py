# accounts/urls.py
from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ProfileAPIView, FollowAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    # profile by username: /accounts/profile/<username>/
    path('profile/<str:username>/', ProfileAPIView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', FollowAPIView.as_view(), name='follow'),
]
