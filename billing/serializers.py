from rest_framework import serializers

from .models import Invoice, DoctorPayout

class InvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'
        depth = 1

class DoctorPayoutSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorPayout
        fields = '__all__'
        depth = 1