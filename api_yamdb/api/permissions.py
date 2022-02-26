"""Модуль содержит самописные пермишены."""
from rest_framework import permissions


class AdminOrReadonly(permissions.BasePermission):
    """Пермишен доступа на чтение для всех на изменение - администратор."""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_admin)
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


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
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author or request.user.is_moderator
            or request.user.is_admin
        )


class AdminOnly(permissions.BasePermission):
    """Пермишен доступа только для админа."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
