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

from .views import (
    # existing views...
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns += [
    path('posts/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),

]

from django.urls import path
from .views import PostSearchView, PostsByTagListView

urlpatterns = [
    # existing paths
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('tags/<slug:tag_slug>/', PostsByTagListView.as_view(), name='posts-by-tag'),
]


