from rest_framework.permissions import BasePermission

class IsInAnyGroup(BasePermission):
    """
    Checks that the user is in a group.
    """
    message = "You must be in a group to perform this operation."

    def has_permission(self, request, view):
        return request.user is not None and request.user.group is not None

class IsInGroup(BasePermission):
    """
    Checks that the user is in the given group.
    """
    message = "You must be in the group to perform this operation."

    def has_object_permission(self, request, view, obj):
        print(request.user.group_id)
        print(obj.pk)
        return request.user.group_id == obj.pk

class IsNotInAnyGroup(BasePermission):
    """
    Checks that the user is not in any group.
    """
    message = "You must leave your current group to perform this operation."

    def has_permission(self, request, view):
        return request.user is not None and request.user.group is None

class IsGroupAdmin(BasePermission):
    """
    Checks that the user is a group admin.
    """
    message = "You must be group admin to perform this operation"

    def has_permission(self, request, view):
        return request.user is not None and request.user.is_group_admin
