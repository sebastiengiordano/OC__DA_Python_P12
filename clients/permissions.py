from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import Saler


class ClientPermission(BasePermission):
    '''Permission for clients.
    
    All salers can add a new client.
    Saler in contact with client can used all others actions.
    Other users have only read permissions.
    '''

    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and
            request.method in SAFE_METHODS or
            request.user.type == "SALER")

    def has_object_permission(self, request, view, obj):
        # Saler in contact with this client has all permissions
        if obj.sales_contact == request.user:
            return True

        # Others users could only have ReadOnly action
        if request.method in SAFE_METHODS:
            return True

        return False
