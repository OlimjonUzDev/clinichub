from rest_framework import viewsets

from .models import Patient
from .serializers import PatientSerializers

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializers

