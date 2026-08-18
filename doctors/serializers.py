from rest_framework import serializers

from .models import Doctor, DoctorSchedule

class DoctorSerializers(serializers.ModelSerializer):
    SENSITIVE_FIELDS = ['bank_name', 'iban', 'revenue_percentage', 'auto_payout', 'is_active', 'user']

    class Meta:
        model = Doctor
        fields = '__all__'

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.role != 'admin':
            for field in self.SENSITIVE_FIELDS:
                validated_data.pop(field, None)
        return super().update(instance, validated_data)

class DoctorScheduleSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = '__all__'