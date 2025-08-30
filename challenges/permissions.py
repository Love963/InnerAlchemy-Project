from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    # Only the challenge creator can update or delete it.
    # Everyone else: read-only (if they can see it).
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "created_by_id", None) == request.user.id
