from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Appointment
from notifications.models import NotificationLog
from notifications.services import send_sms


def _log_and_send(user, phone_number, message):
    """SMS yuboradi va natijani NotificationLog'ga yozadi.
    Xato bo'lsa ham signalni (demak, appointment saqlashni) yiqitmaydi."""
    if not phone_number:
        return
    try:
        result = send_sms(phone_number, message)
        is_sent = bool(result) and 'error' not in result
    except Exception:
        is_sent = False
    NotificationLog.objects.create(user=user, message=message, type='sms', is_sent=is_sent)


@receiver(pre_save, sender=Appointment)
def _stash_old_status(sender, instance, **kwargs):
    """Appointment saqlanishidan oldin uning eski statusini vaqtincha eslab qoladi.

    Bu holat keyinroq post_save signalida status o'zgarganini aniqlash
    (masalan, confirmed yoki cancelled bo'lganini bilish) uchun ishlatiladi.

    Parametrlar:
        sender: signalni yuborgan model klassi (Appointment).
        instance: saqlanayotgan Appointment obyekti.
        kwargs: qo'shimcha signal argumentlari.
    """
    if instance.pk:
        old = Appointment.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
        instance._old_status = old
    else:
        instance._old_status = None


@receiver(post_save, sender=Appointment)
def send_appointment_sms(sender, instance, created, **kwargs):
    """Appointment yaratilganda yoki statusi o'zgarganda bemor va doktorga SMS yuboradi.

    Yangi tashrif yaratilganda bemor va doktorga xabar yuboriladi.
    Status "confirmed" yoki "cancelled"ga o'zgarganda tegishli tomonga
    (kim bekor qilganiga qarab) bildirishnoma yuboriladi.

    Parametrlar:
        sender: signalni yuborgan model klassi (Appointment).
        instance: saqlangan Appointment obyekti.
        created: obyekt yangi yaratilgan bo'lsa True.
        kwargs: qo'shimcha signal argumentlari.
    """
    patient_user = instance.patient.user
    doctor_user = instance.doctor.user
    date_str = instance.start_time.strftime('%Y-%m-%d')
    time_str = instance.start_time.strftime('%H:%M')
    patient_phone = patient_user.phone_number or instance.patient.phone_number

    if created:
        _log_and_send(
            patient_user, patient_phone,
            f"Hurmatli {instance.patient.name_uz}, tashrifingiz {date_str} kuni soat {time_str}ga qabul qilindi.",
        )
        _log_and_send(
            doctor_user, doctor_user.phone_number,
            f"Sizga yangi tashrif band qilindi: {instance.patient.name_uz}, {date_str} soat {time_str}.",
        )
        return

    old_status = getattr(instance, '_old_status', None)
    if old_status and old_status != instance.status:
        if instance.status == 'confirmed':
            _log_and_send(
                patient_user, patient_phone,
                f"Doktor {date_str} soat {time_str}dagi tashrifingizni tasdiqladi.",
            )
        elif instance.status == 'cancelled':
            if instance.cancelled_by_id == patient_user.id:
                _log_and_send(
                    doctor_user, doctor_user.phone_number,
                    f"Bemor {instance.patient.name_uz} {date_str} soat {time_str}dagi tashrifni bekor qildi.",
                )
            else:
                _log_and_send(
                    patient_user, patient_phone,
                    f"{date_str} soat {time_str}dagi tashrifingiz bekor qilindi.",
                )