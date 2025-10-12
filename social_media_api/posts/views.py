from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Post
from .serializers import PostSerializer
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# posts/views.py (append this feed view)

class FeedPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = FeedPagination

    def get_queryset(self):
        user = self.request.user
        # users the user follows
        following_qs = user.following.all()  # because related_name='following' exists
        # optionally include user's own posts too:
        # following_ids = list(following_qs.values_list('id', flat=True)) + [user.id]
        # return Post.objects.filter(author__id__in=following_ids).order_by('-created_at')

        # if you don't want own posts included, omit user.id from list:
        following_ids = list(following_qs.values_list('id', flat=True))
        return Post.objects.filter(author__id__in=following_ids).order_by('-created_at')




class FeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get all posts from users that the current user follows
        user = self.request.user
        following_users = user.following.all()  # 'following' should be the related_name in your User model
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
