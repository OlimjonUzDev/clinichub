from rest_framework import viewsets

from .models import MedicalCenter, ClinicType, Clinic
from .serializers import MedicalCenterSerializers, ClinicTypeSerializers, ClinicSerializers
from users.permissions import IsAdmin

class MedicalCenterViewSet(viewsets.ModelViewSet):
    queryset = MedicalCenter.objects.all()
    serializer_class = MedicalCenterSerializers

class ClinicTypeViewSet(viewsets.ModelViewSet):
    queryset = ClinicType.objects.all()
    serializer_class = ClinicTypeSerializers

class ClinicViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers


# Create your views here.
