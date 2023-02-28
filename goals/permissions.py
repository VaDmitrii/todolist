from rest_framework.permissions import BasePermission


class IsAuthorPermission(BasePermission):
    message = "You don't have permission to such action"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
