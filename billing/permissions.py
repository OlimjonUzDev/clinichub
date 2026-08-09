from rest_framework import permissions

class IsAdminOrOwnerInvoice(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.patient.user == request.user
        return False
    
class IsAdminOrOwnerPayout(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.doctor.user == request.user
        return False 
    
    