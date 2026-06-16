from rest_framework import viewsets

from .models import Appointment
from .serializers import AppointmentSerializers

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers

# Create your views here.
