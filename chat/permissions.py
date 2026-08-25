from rest_framework import permissions

from appointments.models import Appointment

class IsAppointmentParticipant(permissions.BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        appointment_id = view.kwargs.get('appointment_id')
        appointment = Appointment.objects.filter(id=appointment_id).first()
        if appointment is None:
            return False
        if request.user.role == 'admin':
            return True
        return (
            appointment.patient.user == request.user
            or appointment.doctor.user == request.user
        )