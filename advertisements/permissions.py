from rest_framework.permissions import BasePermission

from users.models import User


# ----------------------------------------------------------------------------------------------------------------------
# Create custom permissions
class IsOwnerOrAdmin(BasePermission):
    message: str = 'You are not the owner or administrator'

    def has_object_permission(self, request, view, obj) -> bool:
        return request.user.id == obj.author.id or request.user.role == User.Roles.ADMIN
