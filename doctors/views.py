from rest_framework import viewsets

from .models import Doctor, DoctorSchedule
from .serializers import DoctorSerializers, DoctorScheduleSerializers


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializers

class DoctorScheduleViewSet(viewsets.ModelViewSet):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializers

# Create your views here.
