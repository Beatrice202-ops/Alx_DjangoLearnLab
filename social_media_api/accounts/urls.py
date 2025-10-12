# accounts/urls.py
from django.urls import path
from .views import (
    RegisterAPIView, LoginAPIView, ProfileAPIView, FollowAPIView,  # existing ones
    FollowUserAPIView, UnfollowUserAPIView, FollowersListAPIView, FollowingListAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    # profile by username: /accounts/profile/<username>/
    path('profile/<str:username>/', ProfileAPIView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', FollowAPIView.as_view(), name='follow'),
]



urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', ProfileAPIView.as_view(), name='profile'),

    # follow endpoints
    path('follow/<int:user_id>/', FollowUserAPIView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserAPIView.as_view(), name='unfollow-user'),

    # list followers/following
    path('followers/<int:user_id>/', FollowersListAPIView.as_view(), name='followers-list'),
    path('following/<int:user_id>/', FollowingListAPIView.as_view(), name='following-list'),
]
