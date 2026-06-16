from rest_framework import viewsets

from .models import Appointment, Rating
from .serializers import AppointmentSerializers, RatingSerializers

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers

