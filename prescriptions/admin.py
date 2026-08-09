from django.contrib import admin

from .models import Prescription, PrescriptionItem


class PrescriptionItemInline(admin.TabularInline):
    model = PrescriptionItem
    extra = 1


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'doctor', 'appointment', 'created_at']
    list_filter = ['doctor', 'created_at']
    search_fields = ['patient__name_uz', 'doctor__name_uz', 'diagnosis_uz']
    inlines = [PrescriptionItemInline]


@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'prescription', 'medication_name_uz', 'dosage', 'duration_days']
    search_fields = ['medication_name_uz', 'medication_name_ru']
