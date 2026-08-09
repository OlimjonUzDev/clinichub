from rest_framework import serializers
from django.db import transaction

from .models import Prescription, PrescriptionItem


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        extra_kwargs = {'prescription': {'required': False}}
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):

    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'

    def create(self, validated_data):
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