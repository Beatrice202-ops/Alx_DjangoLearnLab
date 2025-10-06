from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),  # Assuming you have this from before
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)
urlpatterns = [
    # existing auth URLs here...
   path('post/new/', PostCreateView.as_view(), name='post-create'),
path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
