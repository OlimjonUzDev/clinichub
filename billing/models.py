from django.db import models

from appointments.models import Appointment

class Invoice(models.Model):
    INVOICE_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid')
    )
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=225, choices=INVOICE_CHOICES, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.appointment}"
    