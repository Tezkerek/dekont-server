from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    """
    Checks that the user is in a group.
    """
    message = "You must be in a group to perform this operation"

    def has_permission(self, request, view):
        return request.user is not None and request.user.group is not None

class IsNotInGroup(BasePermission):
    """
    Checks that the user is not in a group.
    """
    message = "You must leave your current group to perform this operation"

    def has_permission(self, request, view):
        return request.user is not None and request.user.group is None

class IsGroupAdmin(BasePermission):
    """
    Checks that the user is a group admin.
    """
    message = "You must be group admin to perform this operation"

    def has_permission(self, request, view):
        return request.user is not None and request.user.is_group_admin
