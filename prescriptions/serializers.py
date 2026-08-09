from rest_framework import serializers
from django.db import transaction

from .models import Prescription, PrescriptionItem


class PrescriptionItemSerializer(serializers.ModelSerializer):
    """PrescriptionItem modelini serializatsiya qiladi.

    `prescription` maydoni majburiy emas (extra_kwargs orqali), chunki u odatda
    PrescriptionSerializer.create/update ichida qo'lda biriktiriladi.
    """

    class Meta:
        model = PrescriptionItem
        extra_kwargs = {'prescription': {'required': False}}
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    """Prescription modelini, shu jumladan unga tegishli dori-darmon bandlarini serializatsiya qiladi.

    `items` maydoni faqat o'qish uchun bo'lib, retseptga tegishli barcha
    PrescriptionItem yozuvlarini ko'rsatadi. Dori-darmonlarni yaratish/yangilash
    esa so'rov tanasidagi (request.data) "items" ro'yxati orqali create/update
    metodlarida qo'lda amalga oshiriladi.
    """

    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'

    def create(self, validated_data):
        """Retseptni va unga tegishli dori-darmon bandlarini bitta tranzaksiyada yaratadi.

        So'rov tanasidagi "items" ro'yxatidagi har bir band avval
        PrescriptionItemSerializer orqali tekshiriladi, so'ng Prescription
        yozuvi va barcha bandlar transaction.atomic() ichida saqlanadi.

        Parametrlar:
            validated_data (dict): Prescription modelining tekshirilgan asosiy maydonlari.

        Qaytaradi:
            Prescription: yaratilgan retsept obyekti.

        Xatolar:
            ValidationError: "items" ichidagi biror band noto'g'ri bo'lsa.
        """
        # So'rovdan dorilar listini ajratib olamiz
        items_data = self.context['request'].data.get('items', [])

        item_serializers = []
        for item in items_data:
            serializers = PrescriptionItemSerializer(data=item)
            serializers.is_valid(raise_exception=True)
            item_serializers.append(serializers)

        with transaction.atomic():
            prescription = Prescription.objects.create(**validated_data)
            for serializers in item_serializers:
                serializers.save(prescription=prescription)
        return prescription


    def update(self, instance, validated_data):
        """Mavjud retseptning asosiy maydonlarini va (berilgan bo'lsa) dori-darmon bandlarini yangilaydi.

        "items" so'rovda berilgan bo'lsa, avval barcha yangi bandlar
        PrescriptionItemSerializer orqali tekshiriladi, so'ng eski bandlar
        o'chirilib, yangilari transaction.atomic() ichida saqlanadi. "items"
        berilmasa, mavjud bandlar o'zgarishsiz qoladi.

        Parametrlar:
            instance (Prescription): yangilanayotgan retsept obyekti.
            validated_data (dict): Prescription modelining tekshirilgan asosiy maydonlari.

        Qaytaradi:
            Prescription: yangilangan retsept obyekti.

        Xatolar:
            ValidationError: "items" ichidagi biror band noto'g'ri bo'lsa.
        """
        # Retsept asosiy maydonlarini yangilaymiz
        instance.diagnosis_uz = validated_data.get('diagnosis_uz', instance.diagnosis_uz)
        instance.diagnosis_ru = validated_data.get('diagnosis_ru', instance.diagnosis_ru)
        instance.notes_uz = validated_data.get('notes_uz', instance.notes_uz)
        instance.notes_ru = validated_data.get('notes_ru', instance.notes_ru)

        items_data = self.context['request'].data.get('items', [])
        item_serializers = []
        if items_data:
            for item in items_data:
                serializers = PrescriptionItemSerializer(data=item)
                serializers.is_valid(raise_exception=True)
                item_serializers.append(serializers)
        with transaction.atomic():
            instance.save()
            if items_data:
                instance.items.all().delete()
                for serializers in item_serializers:
                    serializers.save(prescription=instance)
        return instance