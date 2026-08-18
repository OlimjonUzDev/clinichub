from rest_framework import permissions

class IsAdminOrOwnerPrescription(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return request.user.role in ('admin', 'doctor')
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.doctor.user == request.user or obj.patient.user == request.user    
        return obj.doctor.user == request.user
    
class IsAdminOrOwnerPrescriptionItem(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return request.user.role in ('admin', 'doctor')
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.prescription.doctor.user == request.user or obj.prescription.patient.user == request.user
        return obj.prescription.doctor.user == request.user
    