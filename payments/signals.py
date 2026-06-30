from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Payment


@receiver(post_save, sender=Payment)
def update_invoice_on_payment(sender, instance, **kwargs):
    # To'lov muvaffaqiyatli bo'lganda invoice ni avtomatik "paid" ga o'tkazadi
    if instance.status == 'paid':
        invoice = instance.invoice
        invoice.status = 'paid'
        invoice.save(update_fields=['status'])

    # To'lov qaytarilganda invoice ni "refunded" ga o'tkazadi
    elif instance.status == 'refunded':
        invoice = instance.invoice
        invoice.status = 'refunded'
        invoice.save(update_fields=['status'])
