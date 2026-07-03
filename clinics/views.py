from rest_framework import viewsets, filters

from .models import MedicalCenter, ClinicType, Clinic
from .serializers import MedicalCenterSerializers, ClinicTypeSerializers, ClinicSerializers
from users.permissions import IsAdmin

class MedicalCenterViewSet(viewsets.ModelViewSet):
    queryset = MedicalCenter.objects.all()
    serializer_class = MedicalCenterSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class ClinicTypeViewSet(viewsets.ModelViewSet):
    queryset = ClinicType.objects.all()
    serializer_class = ClinicTypeSerializers

class ClinicViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['medical_center__name_uz', 'medical_center__name_ru']

    def get_queryset(self):
        from django.db.models import Count
        return Clinic.objects.annotate(doctors_count=Count('doctor'))


# Create your views here.
