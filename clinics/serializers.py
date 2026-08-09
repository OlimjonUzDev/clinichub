from rest_framework import serializers

from .models import MedicalCenter, ClinicType, Clinic

class MedicalCenterSerializers(serializers.ModelSerializer):
    class Meta:
        model = MedicalCenter
        fields = '__all__'

class ClinicTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = ClinicType
        fields = '__all__'

class ClinicSerializers(serializers.ModelSerializer):
    doctors_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Clinic
        fields = '__all__'