from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class ViewerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.owner == "viewer"


class EmployeePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.owner == "employee"


class BossPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.owner == "boss"


class NoPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return False


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerPark(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.car.owner == request.user or request.user.owner in [
            "boss",
            "employee",
        ]
