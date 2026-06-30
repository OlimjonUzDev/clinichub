from rest_framework import serializers

from .models import Appointment, Rating

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 1

class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        depth = 1