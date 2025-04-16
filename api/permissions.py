from rest_framework import permissions

class IsNurse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'nurse'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsParent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'parent'
