from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from patients.models import Patient
from doctors.models import Doctor
from catalog.models import RankPrice
from clinics.models import Clinic
from users.models import User
from catalog.models import RankPrice

class Appointment(models.Model):
    APPOINTMENT_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    )
    CONSULTATION_CHOICES = RankPrice.CONSULTATION_CHOICES
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=225, choices=APPOINTMENT_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancel_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='cancelled_appointments')
    consultation_type = models.CharField(max_length=225, choices=CONSULTATION_CHOICES, default='in_person')

    def __str__(self):
        return f"{self.patient} -> {self.doctor} ({self.start_time})"

class Rating(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor} - {self.score}/5"
    
