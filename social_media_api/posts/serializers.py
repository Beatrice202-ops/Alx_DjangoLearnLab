from rest_framework import serializers
from .models import Post
from .models import Like
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'created_at']
        
# inside PostSerializer
likes_count = serializers.IntegerField(source='likes.count', read_only=True)

class Meta:
    fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'comments', 'likes_count']

