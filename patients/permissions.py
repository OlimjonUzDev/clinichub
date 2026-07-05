from rest_framework import permissions

class IsAdminOrOwnerPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or obj.user == request.user
    
class IsAdminOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.role in ('admin', 'doctor')