from rest_framework.permissions import BasePermission, SAFE_METHODS


class EventPermission(BasePermission):
    '''Permission for events.

    Admin and manager have all permissions.
    All salers can create a new event.
    Saler who create the event can used all others actions.
    Technician who manage the event can used all others actions.
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

        # Saler who create the event has all permissions
        if obj.contract.saler == request.user:
            return True

        # Technician who manage the event has all permissions
        if obj.technician == request.user:
            return True

        # Others users could only have ReadOnly action
        if request.method in SAFE_METHODS:
            return True

        return False
