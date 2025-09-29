from rest_framework.permissions import BasePermission


class CustomIsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and 
                    (request.user.is_superuser or request.user.is_staff))
