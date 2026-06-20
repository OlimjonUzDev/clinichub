from rest_framework import viewsets

from .models import Clinic
from .serializers import ClinicSerializers
from users.permissions import IsAdmin

class ClinicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers


# Create your views here.
