from django.db import models

from billing.models import Invoice
from patients.models import Patient


class Payment(models.Model):
    PROVIDER_CHOICES = (
        ('payme', 'Payme'),
        ('click', 'Click'),
        ('uzum', 'Uzum Bank'),
        ('cash', 'Naqd pul'),
    )
    STATUS_CHOICES = (
        ('pending', 'Kutilmoqda'),
        ('paid', "To'landi"),
        ('failed', 'Xato'),
        ('cancelled', 'Bekor qilindi'),
        ('refunded', 'Qaytarildi'),
    )

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    stripe_charge_id = models.CharField(max_length=50, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=10, default='UZS')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment #{self.id} — {self.provider} — {self.status}"


class PaymentTransaction(models.Model):
    # To'lov tizimidan kelgan har bir callback/webhook ning to'liq logi
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='transactions')
    raw_data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction #{self.id} — Payment #{self.payment_id}"
