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
    
    # posts/views.py (edit PostViewSet)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from .models import Like, Post, Comment
from .serializers import PostSerializer, CommentSerializer, LikeSerializer

class PostViewSet(viewsets.ModelViewSet):
    # ... existing code ...

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        # Prevent duplicate likes
        like, created = Like.objects.get_or_create(post=post, user=user)
        if not created:
            return Response({'detail': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

        # create notification for post author if not liking own post
        if post.author != user:
            Notification.objects.create(
                recipient=post.author,
                actor=user,
                verb='liked your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=str(post.pk)
            )

        return Response({'detail': 'Post liked'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.delete()
            return Response({'detail': 'Post unliked'}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({'detail': 'Not liked yet'}, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    # ... existing code ...

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        post = comment.post
        # notify post author if commenter is not the author
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=self.request.user,
                verb='commented on your post',
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=str(post.pk)
            )
