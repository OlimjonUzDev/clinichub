from rest_framework import viewsets, filters

from .models import Doctor, DoctorSchedule
from .serializers import DoctorSerializers, DoctorScheduleSerializers
from users.permissions import IsAdmin


class DoctorViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']
    

class DoctorScheduleViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializers

# Create your views here.
