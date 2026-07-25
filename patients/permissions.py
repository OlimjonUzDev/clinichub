from rest_framework import permissions

class IsAdminOrOwnerPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        return request.user.role == 'admin' or obj.user == request.user
    
class IsAdminOrDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
            return request.user.is_authenticated and request.user.role in ('admin', 'doctor')