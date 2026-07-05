from rest_framework import permissions

class IsAdminOrOwnerDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated
    
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or obj.user == request.user
    
class IsAdminOrOwnerSchedule(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        if not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return request.user.role in ('admin', 'doctor')
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or obj.doctor.user == request.user
        