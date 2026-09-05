from django.db.models.signals import post_save
from django.dispatch import receiver

from appointments.models import Appointment
from catalog.models import RankPrice
from .models import Invoice


@receiver(post_save, sender=Appointment)
def create_invoice_on_confirmation(sender, instance, created, **kwargs):
    if created or instance.status != 'confirmed':
        return
    if Invoice.objects.filter(appointment=instance).exists():
        return

    rank_price = RankPrice.objects.filter(
        rank_type=instance.doctor.rank_type_id,
        clinic=instance.clinic_id,
        consultation_type=instance.consultation_type,
        is_active=True,
    ).first()

    Invoice.objects.create(
        appointment=instance,
        patient=instance.patient,
        invoice_number=f"INV-{instance.id:06d}",
        amount=rank_price.price if rank_price else 0,
        currency=rank_price.currency if rank_price else 'UZS',
        status='pending',
    )