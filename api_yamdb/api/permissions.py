from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Доступ только для администратора проекта."""

    def has_permission(self, request, view):
        return request.user.is_admin

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class IsModerator(BasePermission):
    """Доступ только для модератора проекта."""

    def has_permission(self, request, view):
        return request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class ReadOnly(BasePermission):
    """Доступ только на чтение."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS


class OwnerOnly(BasePermission):
    """Доступ только владельцу."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
