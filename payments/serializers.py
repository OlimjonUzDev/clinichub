from rest_framework import serializers

from .models import Payment, PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTransaction
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    # GET da webhook loglari ham birga chiqadi
    transactions = PaymentTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        # Bu maydonlar faqat to'lov tizimi tomonidan to'ldiriladi
        read_only_fields = ['status', 'transaction_id', 'paid_at', 'created_at', 'stripe_charge_id']

    def validate(self, attrs):
        invoice = attrs.get('invoice')
        amount = attrs.get('amount')
        request = self.context.get('request')

        if request and request.user.role != 'admin':
            if invoice and invoice.patient.user != request.user:
                raise serializers.ValidationError('Bu invoice sizga tegishli emas')
            if attrs.get('patient') and attrs['patient'].user != request.user:
                raise serializers.ValidationError('Boshqa bemor nomidan tolov yarat olmaysiz')

        
        if invoice and invoice.status == 'paid':
            raise serializers.ValidationError("Bu invoice allaqachon to'langan.")

        
        if invoice and amount and amount != invoice.amount:
            raise serializers.ValidationError(
                f"Summa mos emas. To'g'ri summa: {invoice.amount} UZS."
            )

        return attrs

