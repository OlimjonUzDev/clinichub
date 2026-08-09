from rest_framework import serializers

from .models import Patient

class PatientSerializers(serializers.ModelSerializer):
    """``Patient`` modelining barcha maydonlarini serializatsiya qiladi va tekshiradi."""

    class Meta:
        """``PatientSerializers`` uchun model va maydonlar sozlamalari."""

        model = Patient
        fields = '__all__'