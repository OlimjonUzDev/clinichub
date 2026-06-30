from rest_framework import serializers

from .models import Prescription, PrescriptionItem


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    # GET da dorilar ro'yxati ham birga chiqadi
    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'

    def create(self, validated_data):
        # So'rovdan dorilar listini ajratib olamiz
        items_data = self.context['request'].data.get('items', [])

        # Avval retseptni saqlaymiz
        prescription = Prescription.objects.create(**validated_data)

        # Keyin har bir dorini saqlaymiz
        for item in items_data:
            PrescriptionItem.objects.create(prescription=prescription, **item)

        return prescription

    def update(self, instance, validated_data):
        # Retsept asosiy maydonlarini yangilaymiz
        instance.diagnosis_uz = validated_data.get('diagnosis_uz', instance.diagnosis_uz)
        instance.diagnosis_ru = validated_data.get('diagnosis_ru', instance.diagnosis_ru)
        instance.notes_uz = validated_data.get('notes_uz', instance.notes_uz)
        instance.notes_ru = validated_data.get('notes_ru', instance.notes_ru)
        instance.save()

        # Agar yangi dorilar yuborilgan bo'lsa — eskisini o'chirib yangisini yozamiz
        items_data = self.context['request'].data.get('items', [])
        if items_data:
            instance.items.all().delete()
            for item in items_data:
                PrescriptionItem.objects.create(prescription=instance, **item)

        return instance
