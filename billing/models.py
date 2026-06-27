from django.db import models

from appointments.models import Appointment
from patients.models import Patient
from doctors.models import Doctor

class Invoice(models.Model):
    INVOICE_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded')
    )
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=225, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='UZS')
    is_tax_inclusive = models.BooleanField(default=True)
    status = models.CharField(max_length=225, choices=INVOICE_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.appointment}"
    
class InsuranceClaim(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    )
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    claim_number = models.CharField(max_length=225)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
class DoctorPayout(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid')
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period_from = models.DateField()
    period_to = models.DateField()
    status = models.CharField(max_length=225, choices=STATUS_CHOICES)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
