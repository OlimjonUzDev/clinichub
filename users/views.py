from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegisterSerializers, UserSerializers
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from .permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializers


class DashboardView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        from clinics.models import Clinic
        return Response({
            'total_doctors':              Doctor.objects.count(),
            'total_patients':             Patient.objects.count(),
            'total_appointments':         Appointment.objects.count(),
            'total_clinics':              Clinic.objects.count(),
            'upcoming_appointments':      Appointment.objects.filter(status='pending').count(),
            'ongoing_appointments':       Appointment.objects.filter(status='confirmed').count(),
            'completed_appointments':     Appointment.objects.filter(status='completed').count(),
            'cancelled_appointments':     Appointment.objects.filter(status='cancelled').count(),
        })

