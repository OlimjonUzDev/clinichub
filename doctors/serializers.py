from rest_framework import serializers

from .models import Doctor, DoctorSchedule

class DoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'
        # depth = 1

class DoctorScheduleSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'