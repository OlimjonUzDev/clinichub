from rest_framework import serializers
from django.db import transaction

from .models import Prescription, PrescriptionItem


class PrescriptionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionItem
        extra_kwargs = {'prescription': {'required': False}}
        fields = '__all__'

    def validate(self, attrs):
        prescription = attrs.get('prescription')
        if prescription:
            request = self.context['request']
            if request.user.role == 'doctor' and prescription.doctor.user != request.user:
                raise serializers.ValidationError("Bu retsept sizga tegishli emas.")
        return attrs


class PrescriptionSerializer(serializers.ModelSerializer):

    items = PrescriptionItemSerializer(many=True, read_only=True)

    class Meta:
        model = Prescription
        fields = '__all__'
        read_only_fields = ['doctor', 'patient']

    def validate(self, attrs):
        appointment = attrs.get('appointment') or self.instance.appointment
        request = self.context['request']
        if request.user.role == 'doctor' and appointment.doctor.user != request.user:
            raise serializers.ValidationError("Bu appointment sizga tegishli emas")
        if appointment.status != 'completed':
            raise serializers.ValidationError("Retsept faqat 'completed' holatidagi appointment uchun yoziladi")
        return attrs
    

    def create(self, validated_data):
        appointment = validated_data['appointment']
        validated_data['doctor'] = appointment.doctor
        validated_data['patient'] = appointment.patient
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