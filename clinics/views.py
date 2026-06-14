from rest_framework import viewsets

from .models import Clinic
from .serializers import ClinicSerializers

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers


# Create your views here.
