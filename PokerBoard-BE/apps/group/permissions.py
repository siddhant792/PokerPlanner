from rest_framework import permissions


class IsGroupAdminPermission(permissions.BasePermission):
    """
    Permission check for group admin permission
    """

    def has_object_permission(self, request, view, group):
        """
        Checks if the group is created by current logged in user.
        """
        return request.user == group.created_by
