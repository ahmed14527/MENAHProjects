from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsNurse(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'nurse'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'parent'

class IsNurseOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.role == 'nurse'
