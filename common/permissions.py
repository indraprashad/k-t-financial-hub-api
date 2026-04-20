from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow anyone to read (GET, HEAD, OPTIONS)
    Only admin/staff can write (POST, PUT, PATCH, DELETE)
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsSuperAdmin(permissions.BasePermission):
    """
    Only super_admin role or Django superuser can perform this action
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        # Check if user is Django superuser
        if request.user.is_superuser:
            return True
        # Check if user has super_admin role
        try:
            return request.user.role_assignment.role.name == 'super_admin'
        except AttributeError:
            return False
