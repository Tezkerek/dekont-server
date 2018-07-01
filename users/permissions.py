from rest_framework.permissions import BasePermission

class IsUserOrGroupAdmin(BasePermission):
    """
    For use with a user queryset.
    """
    message = "You must be the user or the group admin to perform this operation."

    def has_object_permission(self, request, view, obj):
        return request.user.is_group_admin or request.user == obj
