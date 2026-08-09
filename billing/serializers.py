from rest_framework import serializers

from .models import Invoice, DoctorPayout

class InvoiceSerializers(serializers.ModelSerializer):
    """Invoice modelining barcha maydonlarini serializatsiya qiladi.

    Maxsus validatsiya metodlari mavjud emas, barcha maydonlar (`fields = '__all__'`)
    orqali kiritiladi/qaytariladi.
    """
    class Meta:
        model = Invoice
        fields = '__all__'

class DoctorPayoutSerializers(serializers.ModelSerializer):
    """DoctorPayout modelining barcha maydonlarini serializatsiya qiladi.

    Maxsus validatsiya metodlari mavjud emas, barcha maydonlar (`fields = '__all__'`)
    orqali kiritiladi/qaytariladi.
    """
    class Meta:
        model = DoctorPayout
        fields = '__all__'