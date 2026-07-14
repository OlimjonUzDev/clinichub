from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Doctor

@receiver(post_save, sender=Doctor)
def sync_user_role_to_doctor(sender, instance, **kwargs):
    if instance.user.role != 'doctor':
        instance.user.role = 'doctor'
        instance.user.save(update_fields=['role'])