from rest_framework.permissions import BasePermission

from users.models import Saler, Technician


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_admin)


class IsSalerAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.type == "SALER")


class IsTechnicianAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.type == "TECHNICIAN")
