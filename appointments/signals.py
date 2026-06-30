from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from notifications.services import send_sms

@receiver(post_save, sender=Appointment)
def send_appointment_sms(sender, instance, created, **kwargs):
    if created:
        phone_number = instance.patient.user.phone_number
        message = f"Hurmatli {instance.patient.user.username}, sizning navbatingiz {instance.start_time.strftime('%Y-%m-%d')} kuni soat {instance.start_time.strftime('%H:%M')}ga qabul qilindi"
        send_sms(phone_number, message)