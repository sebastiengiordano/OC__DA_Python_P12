from rest_framework.permissions import BasePermission, SAFE_METHODS


class ClientPermission(BasePermission):
    '''Permission for clients.'''

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Admin has all permissions
        if request.user.is_admin:
            return True

        # Saler has all permissions
        if obj.sales_contact == request.user:
            return True

        # Others users could only has read action
        if request.method in SAFE_METHODS:
            return True

        return False
