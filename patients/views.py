from rest_framework import viewsets, filters

from .models import Patient
from .serializers import PatientSerializers
from .permissions import IsAdminOrDoctor, IsAdminOrOwnerPatient
from users.permissions import IsAdmin

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminOrDoctor()]
        if self.action in ['create', 'destroy']:
            return [IsAdmin()]
        return [IsAdminOrOwnerPatient()]

