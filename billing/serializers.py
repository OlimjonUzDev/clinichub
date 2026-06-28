from rest_framework import serializers

from .models import Invoice, InsuranceClaim, DoctorPayout

class InvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class InsuranceClaimSerializers(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        fields = '__all__'

class DoctorPayoutSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorPayout
        fields = '__all__'