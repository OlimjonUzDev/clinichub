from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import User
from .serializers import RegisterSerializers
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from .permissions import IsAdmin



class RegisterView(generics.CreateAPIView):
    # permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializers
   

class DashboardView(APIView):
    # permission_classes = [IsAdmin]
    def get(self, request):
        return Response({
            'total_doctors': Doctor.objects.count(),
            'total_patients': Patient.objects.count(),
            'total_appointments': Appointment.objects.count()
        })

