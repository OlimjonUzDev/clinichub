from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import User, OTPCode

class UserSerializers(serializers.ModelSerializer):
    """User modelini parol maydonisiz (barcha boshqa maydonlar bilan) serializatsiya qiladi."""

    class Meta:
        model = User
        exclude = ['password']

class RegisterSerializers(serializers.ModelSerializer):
    """Yangi foydalanuvchini ro'yxatdan o'tkazish uchun ma'lumotlarni valid qiladi va yaratadi.

    Yaratilgan foydalanuvchiga so'rov tanasidagi qiymatidan qat'i nazar,
    har doim 'patient' roli beriladi. Parol maydoni faqat yozish uchun
    (write_only) va Django'ning standart parol validatorlari orqali tekshiriladi.
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'phone_number']

    def create(self, validated_data):
        """Rolini majburan 'patient' qilib, yangi foydalanuvchini yaratadi.

        Parametrlar:
            validated_data: Valid qilingan foydalanuvchi ma'lumotlari.

        Qaytaradi:
            Yaratilgan User obyekti.
        """
        validated_data['role'] = 'patient'
        return User.objects.create_user(**validated_data)

    def validate_password(self, value):
        """Parolni Django'ning standart parol kuchliligi validatorlari orqali tekshiradi.

        Parametrlar:
            value: Tekshirilayotgan parol qiymati.

        Qaytaradi:
            Valid parol qiymati.

        Xatolar:
            ValidationError: Parol kuchsiz yoki qoidalarga mos kelmasa.
        """
        validate_password(value)
        return value

    password = serializers.CharField(write_only=True)

class OTPRequestSerializers(serializers.Serializer):
    """OTP kod so'rash uchun telefon raqamini valid qiladi."""
    phone_number = serializers.CharField()

class OTPVerifySerializers(serializers.Serializer):
    """OTP kodni tasdiqlash uchun telefon raqami va kodni valid qiladi."""
    phone_number = serializers.CharField()
    code = serializers.CharField(max_length=6)
