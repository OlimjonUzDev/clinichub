from rest_framework import serializers

from .models import Patient

class PatientSerializers(serializers.ModelSerializer):
    SENSITIVE_FIELDS = ['user']

    class Meta:
        model = Patient
        fields = '__all__'

    def update(self, instance, validated_data):
        request = self.context.get('request')
        if request and request.user.role != 'admin':
            for field in self.SENSITIVE_FIELDS:
                validated_data.pop(field, None)
        return super().update(instance, validated_data)