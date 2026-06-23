from rest_framework import viewsets

from .models import Appointment, Rating
from .serializers import AppointmentSerializers, RatingSerializers
from rest_framework.permissions import IsAuthenticated

class AppointmentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers

class RatingViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers

