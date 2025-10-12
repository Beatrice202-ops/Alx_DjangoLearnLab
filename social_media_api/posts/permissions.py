# posts/permissions.py
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read-only requests for anyone, but write requests only for the owner.
    """
    def has_object_permission(self, request, view, obj):
        # Read permission for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to the object's owner (author)
        return obj.author == request.user
