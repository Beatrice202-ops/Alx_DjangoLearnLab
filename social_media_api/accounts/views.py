from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth import login
from .models import User

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user, context={'request': request}).data
        return Response({"user": user_data, "token": token.key}, status=status.HTTP_201_CREATED)

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        # Optionally log the user into the session (not necessary for token auth)
        login(request, user)
        return Response({"token": token.key, "user": UserSerializer(user, context={'request': request}).data}, status=status.HTTP_200_OK)

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'username'
    queryset = User.objects.all()

    # GET /profile/<username> to view profile
    # PATCH /profile/<username> to update (only allowed for owner)
    def get_object(self):
        obj = super().get_object()
        return obj

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            return Response({"detail": "You do not have permission to edit this profile."}, status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        """Toggle follow/unfollow for target user."""
        try:
            target = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.user == target:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in target.followers.all():
            # already following => unfollow
            target.followers.remove(request.user)
            action = "unfollowed"
        else:
            target.followers.add(request.user)
            action = "followed"

        return Response({"detail": f"{action} {target.username}", "followers_count": target.followers.count()})

