from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import User
from .serializers import RegisterSerializers
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment



class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializers

class DashboardView(APIView):
    def get(self, request):
        return Response({
            'total_doctors': Doctor.objects.count(),
            'total_patients': Patient.objects.count(),
            'total_appointments': Appointment.objects.count()
        })

