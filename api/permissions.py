from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsNurseUser(permissions.BasePermission):
    """
    Allows access only to nurse users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'nurse'

class IsAdminOrOwner(permissions.BasePermission):
    """
    Object-level permission to allow admins or owners to edit an object.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.role == 'admin'
    
    
    
class IsParentUser(permissions.BasePermission):
    """
    Allows access only to parent users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'parent'

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object or admin users to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.role == 'admin'

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow read-only access for non-admin users.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin'

class IsNurseCanVerify(permissions.BasePermission):
    """
    Allows verification access to nurses only.
    """
    def has_permission(self, request, view):
        return request.user.role == 'nurse'

class IsAdminCanApproveUsers(permissions.BasePermission):
    """
    Allows only admins to approve or disapprove users.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsAdminOrNurseCanView(permissions.BasePermission):
    """
    Allows access to both admin and nurse users for viewing.
    """
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.role == 'nurse'
