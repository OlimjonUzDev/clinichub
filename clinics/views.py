from rest_framework import viewsets, filters
from django.db.models import Count

from .models import MedicalCenter, ClinicType, Clinic
from .serializers import MedicalCenterSerializers, ClinicTypeSerializers, ClinicSerializers
from users.permissions import IsAdminOrReadOnly

class MedicalCenterViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = MedicalCenter.objects.all()
    serializer_class = MedicalCenterSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class ClinicTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = ClinicType.objects.all()
    serializer_class = ClinicTypeSerializers

class ClinicViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['medical_center__name_uz', 'medical_center__name_ru']

    def get_queryset(self):
        return Clinic.objects.annotate(doctors_count=Count('doctor'))


# Create your views here.
