from rest_framework import serializers

from .models import Payment, PaymentTransaction


class PaymentTransactionSerializer(serializers.ModelSerializer):
    """PaymentTransaction modelini (webhook logi) to'liq serializatsiya qiladi."""

    class Meta:
        model = PaymentTransaction
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """Payment modelini serializatsiya qiladi va yaratishda invoice/summani tekshiradi.

    transactions maydoni orqali GET so'rovida tegishli webhook loglari
    (PaymentTransaction) ham birga qaytariladi. status, transaction_id,
    paid_at, created_at va stripe_charge_id maydonlari faqat o'qish uchun
    (to'lov tizimi tomonidan to'ldiriladi).
    """

    # GET da webhook loglari ham birga chiqadi
    transactions = PaymentTransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        # Bu maydonlar faqat to'lov tizimi tomonidan to'ldiriladi
        read_only_fields = ['status', 'transaction_id', 'paid_at', 'created_at', 'stripe_charge_id']

    def validate(self, attrs):
        """To'lov yaratishdan oldin egalik, invoice statusi va summa mosligini tekshiradi.

        Admin bo'lmagan foydalanuvchi faqat o'ziga tegishli invoice/patient
        uchun to'lov yarata olishini, invoice allaqachon to'lanmaganligini
        va kiritilgan summa invoice summasiga mos kelishini tekshiradi.

        Parametrlar:
            attrs: Tekshirilayotgan (validatsiyadan o'tayotgan) maydonlar lug'ati.

        Qaytaradi:
            Tekshiruvdan o'tgan attrs lug'atini.

        Xatolar:
            serializers.ValidationError: Egalik mos kelmasa, invoice
                allaqachon to'langan bo'lsa yoki summalar mos kelmasa.
        """
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

