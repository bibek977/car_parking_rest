from rest_framework import permissions
from django.contrib.auth import get_user_model

User=get_user_model()
    
class ViewerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.owner=="viewer"

class EmployeePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.owner=='employee'

class BossPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.owner=='boss'
    
class OwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user