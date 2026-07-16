from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Appointment, Rating
from .serializers import AppointmentSerializers, RatingSerializers
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsPatient
from .permissions import IsAdminOrOwnerAppointments, IsAdminOrOwnerRating

class CustomPagination(PageNumberPagination):
    page_size = 6

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['patient__name_uz', 'patient__name_ru']

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAuthenticated()]
        return [IsAdminOrOwnerAppointments()]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsPatient()]
        return [IsAdminOrOwnerRating()]

