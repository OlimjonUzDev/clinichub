from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated

from .models import Doctor, DoctorSchedule
from .serializers import DoctorSerializers, DoctorScheduleSerializers
from .permissions import IsAdminOrOwnerDoctor, IsAdminOrOwnerSchedule
from users.permissions import IsAdminOrReadOnly


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action in ['create', 'destroy']:
            return [IsAdminOrReadOnly()]
        return [IsAdminOrOwnerDoctor()]
    

class DoctorScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrOwnerSchedule()]
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializers


