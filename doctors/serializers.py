from rest_framework import serializers

from .models import Doctor, DoctorSchedule

class DoctorSerializers(serializers.ModelSerializer):
    """``Doctor`` modelining barcha maydonlarini serializatsiya qiladi."""

    class Meta:
        """Serializatsiya qilinadigan model va maydonlarni belgilaydi."""

        model = Doctor
        fields = '__all__'

class DoctorScheduleSerializers(serializers.ModelSerializer):
    """``DoctorSchedule`` modelining barcha maydonlarini serializatsiya qiladi."""

    class Meta:
        """Serializatsiya qilinadigan model va maydonlarni belgilaydi."""

        model = DoctorSchedule
        fields = '__all__'