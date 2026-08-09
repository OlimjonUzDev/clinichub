from django.db import models

from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient


class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='prescription')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    diagnosis_uz = models.TextField()
    diagnosis_ru = models.TextField(blank=True)
    notes_uz = models.TextField(blank=True)
    notes_ru = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Retsept #{self.id} — {self.patient}"


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medication_name_uz = models.CharField(max_length=255)
    medication_name_ru = models.CharField(max_length=255, blank=True)
    dosage = models.CharField(max_length=100)        # masalan: "500mg", "1 dona"
    frequency_uz = models.CharField(max_length=255)  # masalan: "kuniga 3 marta"
    frequency_ru = models.CharField(max_length=255, blank=True)
    duration_days = models.PositiveIntegerField()    # necha kun ichish kerak
    notes_uz = models.TextField(blank=True)
    notes_ru = models.TextField(blank=True)

    def __str__(self):
        return f"{self.medication_name_uz} — {self.dosage}"
