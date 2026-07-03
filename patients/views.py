from rest_framework import viewsets, filters

from .models import Patient
from .serializers import PatientSerializers
from users.permissions import IsAdmin

class PatientViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

