from rest_framework import viewsets

from .models import Patient
from .serializers import PatientSerializers
from users.permissions import IsAdmin

class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializers

