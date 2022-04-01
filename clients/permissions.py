from rest_framework.permissions import BasePermission, SAFE_METHODS


class ClientPermission(BasePermission):
    '''Permission for clients.

    Admin and manager have all permissions.
    All salers can add a new client.
    Saler in contact with client can used all others actions.
    Other users have only read permissions.
    '''

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_admin or
            request.method in SAFE_METHODS or
            request.user.type == "SALER")

    def has_object_permission(self, request, view, obj):
        # Admin and manager have all permissions
        if request.user.is_admin:
            return True

        # Saler in contact with this client has all permissions
        if obj.sales_contact == request.user:
            return True

        # Others users could only have ReadOnly action
        if request.method in SAFE_METHODS:
            return True

        return False
