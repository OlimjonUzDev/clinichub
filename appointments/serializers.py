from rest_framework import serializers
from django.utils import timezone

from .models import Appointment, Rating
from doctors.models import DoctorSchedule

class AppointmentSerializers(serializers.ModelSerializer):
    """Appointment modelini serializatsiya qiladi va band qilish qoidalarini tekshiradi.

    Vaqt oralig'ining to'g'riligini, doktorning boshqa tashrif bilan
    band emasligini va tashrif vaqti doktorning ish jadvaliga mos
    kelishini validate() metodida tekshiradi.
    """

    class Meta:
        """Appointment modeli va barcha maydonlar uchun serializer sozlamalari."""

        model = Appointment
        fields = '__all__'

    def validate(self, attrs):
        """Tashrif vaqti, doktorning bandligi va ish jadvalini tekshiradi.

        Parametrlar:
            attrs: tekshirilayotgan (start_time, end_time, doctor va h.k.) maydonlar.

        Qaytaradi:
            dict: tekshiruvdan o'tgan attrs.

        Xatolar:
            ValidationError: tugash vaqti boshlanishdan oldin bo'lsa,
                doktor shu vaqtda band bo'lsa, doktor shu kuni ishlamasa
                yoki vaqt ish jadvalidan tashqarida bo'lsa.
        """
        start = attrs.get('start_time', getattr(self.instance, 'start_time', None))
        end = attrs.get('end_time', getattr(self.instance, 'end_time', None))
        doctor = attrs.get('doctor', getattr(self.instance, 'doctor', None))

        if start and end and end <= start:
            raise serializers.ValidationError("Tugash vaqti boshlanish vaqtidan keyin bo'lishi kerak")

        if doctor and start and end:
            overlapping = Appointment.objects.filter(doctor=doctor, start_time__lt=end, end_time__gt=start,).exclude(status='cancelled')
            if self.instance:
                overlapping = overlapping.exclude(pk=self.instance.pk)
            if overlapping.exists():
                raise serializers.ValidationError("Doktor bu vaqt band")

            local_start = timezone.localtime(start)
            local_end = timezone.localtime(end)
            schedule = DoctorSchedule.objects.filter(doctor=doctor, weekday=local_start.weekday()).first()
            if not schedule:
                raise serializers.ValidationError('Doktor bu kun ishlamaydi')
            if local_start.time() < schedule.start_time or local_end.time() > schedule.end_time:
                raise serializers.ValidationError("Vaqt doktorning ish jadvalidan tashqarida")
        return attrs

class RatingSerializers(serializers.ModelSerializer):
    """Rating modelini serializatsiya qiladi va baho qo'yish huquqini tekshiradi.

    patient va doctor maydonlari read-only bo'lib, ular tashrifdan
    avtomatik olinadi. validate() faqat tashrif egasi bemor (yoki admin)
    va faqat yakunlangan tashrif uchun baho qo'yishga ruxsat beradi.
    """

    class Meta:
        """Rating modeli va o'qish uchun yopiq (patient, doctor) maydonlar sozlamasi."""

        model = Rating
        fields = '__all__'
        read_only_fields = ['patient', 'doctor']

    def validate(self, attrs):
        """Bahoni faqat tashrif egasi bemor va faqat yakunlangan tashrif uchun ruxsat beradi.

        Parametrlar:
            attrs: tekshirilayotgan maydonlar, jumladan appointment.

        Qaytaradi:
            dict: tekshiruvdan o'tgan attrs.

        Xatolar:
            ValidationError: so'rov yuboruvchi tashrif egasi bo'lmasa
                yoki tashrif hali yakunlanmagan bo'lsa.
        """
        request = self.context['request']
        appointment = attrs.get('appointment', getattr(self.instance, 'appointment', None))

        if appointment and request.user.role != 'admin':
            patient = getattr(request.user, 'patient', None)
            if not patient or appointment.patient_id != patient.id:
                raise serializers.ValidationError("Bu tashrifga baho qo'yish huquqingiz yo'q")

        if appointment and appointment.status != 'completed':
            raise serializers.ValidationError("Faqat yakunlangan tashrif uchun baho qoldirish mumkun")

        return attrs