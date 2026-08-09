from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Doctor

@receiver(post_save, sender=Doctor)
def sync_user_role_to_doctor(sender, instance, **kwargs):
    """``Doctor`` obyekti saqlanganda foydalanuvchi rolini 'doctor'ga moslashtiradi.

    ``Doctor.save()`` chaqirilganda (post_save signali) ishga tushadi.
    Agar bog'langan foydalanuvchining ``role`` maydoni 'doctor' bo'lmasa,
    uni 'doctor'ga o'zgartirib, faqat shu maydonni saqlaydi.

    Parametrlar:
        sender: Signalni yuborgan model klassi (``Doctor``).
        instance: Saqlangan ``Doctor`` obyekti.
        **kwargs: Django signali tomonidan uzatiladigan qo'shimcha argumentlar.
    """
    if instance.user.role != 'doctor':
        instance.user.role = 'doctor'
        instance.user.save(update_fields=['role'])