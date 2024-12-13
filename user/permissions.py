from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated

from user.choices import UserTypeChoices


class ActiveUserPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.verified


class AdminsOnlyPermission(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.is_superuser


class LoggedInReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.method in SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.method in SAFE_METHODS
