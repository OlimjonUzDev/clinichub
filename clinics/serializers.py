from rest_framework import serializers

from .models import Clinic

class ClinicSerializers(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'