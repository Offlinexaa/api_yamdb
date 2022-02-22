from rest_framework import permissions


class AdminOrReadonly(permissions.BasePermission):
    """Пермишен доступа на чтение для всех на изменение - администратор."""
    def has_permission(self, request, view):
        result = False
        result = result or request.method in permissions.SAFE_METHODS
        result = result or request.user.is_superuser
        if request.user.is_authenticated:
            result = result or request.user.role.lower() == 'admin'
        return result

    def has_object_permission(self, request, view, obj):
        return self.has_permission()


class AuthorModeratorAdminOrReadonly(permissions.BasePermission):
    """
    Пермишен доступа на чтение для всех на изменение:
    автор, модератор или администратор.
    """
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        result = False
        result = result or request.method in permissions.SAFE_METHODS
        result = result or request.user == obj.author
        result = result or request.user.is_superuser
        if request.user.is_authenticated:
            result = result or request.user.role.lower() == 'moderator'
            result = result or request.user.role.lower() == 'admin'
        return result


class AdminOnly(permissions.BasePermission):
    """Пермишен доступа только для админа."""
    def has_permission(self, request, view):
        result = False
        result = result or request.user.is_superuser
        if request.user.is_authenticated:
            result = result or request.user.role.lower() == 'admin'
        return result

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
