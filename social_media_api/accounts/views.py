from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


User = get_user_model()

# Register View
class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_201_CREATED)


# Login View
class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


# Profile View
class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "username": user.username,
            "email": user.email,
        }
        return Response(data)


# Follow View (optional for now)
class FollowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        return Response({"message": "Follow functionality not yet implemented"})
    
    # accounts/views.py (append or create these views)

User = get_user_model()


class FollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # follow user with id=user_id
        target = get_object_or_404(User, id=user_id)

        if request.user == target:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        # Using the existing ManyToMany: add request.user to target.followers
        target.followers.add(request.user)
        return Response({"detail": f"You are now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # unfollow user with id=user_id
        target = get_object_or_404(User, id=user_id)

        if request.user == target:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        target.followers.remove(request.user)
        return Response({"detail": f"You have unfollowed {target.username}."}, status=status.HTTP_200_OK)


class FollowersListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        # Return list of follower usernames and ids
        data = [{"id": u.id, "username": u.username} for u in target.followers.all()]
        return Response({"followers": data})

class FollowingListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        target = get_object_or_404(User, id=user_id)
        # 'following' is the related_name on the followers M2M, so target.following.all() are users target follows
        data = [{"id": u.id, "username": u.username} for u in target.following.all()]
        return Response({"following": data})
    
    # accounts/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import CustomUser

class FollowAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Get all users
        users = CustomUser.objects.all()
        # Find the user to follow
        user_to_follow = get_object_or_404(users, id=user_id)
        # Prevent self-follow
        if request.user == user_to_follow:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        # Add follow
        request.user.following.add(user_to_follow)
        return Response({"detail": f"You are now following {user_to_follow.username}."}, status=status.HTTP_200_OK)


class UnfollowAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Get all users
        users = CustomUser.objects.all()
        # Find the user to unfollow
        user_to_unfollow = get_object_or_404(users, id=user_id)
        # Remove follow
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)



