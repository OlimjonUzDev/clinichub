from rest_framework import serializers

from .models import Invoice

class InvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'