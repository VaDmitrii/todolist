from rest_framework.permissions import BasePermission


class AdminOrAuthorPermission(BasePermission):
    message = "You don't have permission to such action"

    def has_object_permission(self, request, view, obj):
        if request.user == (obj.user if obj.user else obj.owner):
            return True
        else:
            return request.user.is_admin