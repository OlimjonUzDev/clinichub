from rest_framework import serializers

from .models import MedicalCenter, ClinicType, Clinic

class MedicalCenterSerializers(serializers.ModelSerializer):
    """``MedicalCenter`` modelini barcha maydonlari bilan serialize qiladi."""

    class Meta:
        model = MedicalCenter
        fields = '__all__'

class ClinicTypeSerializers(serializers.ModelSerializer):
    """``ClinicType`` modelini barcha maydonlari bilan serialize qiladi."""

    class Meta:
        model = ClinicType
        fields = '__all__'

class ClinicSerializers(serializers.ModelSerializer):
    """``Clinic`` modelini serialize qiladi.

    ``doctors_count`` — view darajasida annotatsiya qilinadigan,
    faqat o'qish uchun mo'ljallangan hisoblangan maydon (klinikadagi
    shifokorlar soni).
    """

    doctors_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Clinic
        fields = '__all__'