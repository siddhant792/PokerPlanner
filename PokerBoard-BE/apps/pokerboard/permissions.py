from rest_framework import permissions


class IsManagerPermission(permissions.BasePermission):
    """
    Permission check for pokerboard manager
    """

    def has_object_permission(self, request, view, pokerboard):
        return request.user == pokerboard.manager
