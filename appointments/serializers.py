from rest_framework import serializers
from django.utils import timezone

from .models import Appointment, Rating
from doctors.models import DoctorSchedule

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['status', 'cancelled_by']

    def validate(self, attrs):
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

    def update(self, instance, validated_data):
        validated_data.pop('patient', None)
        validated_data.pop('doctor', None)
        return super().update(instance, validated_data)

class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ['patient', 'doctor', 'appointment']

    def validate(self, attrs):
        request = self.context['request']
        appointment = attrs.get('appointment', getattr(self.instance, 'appointment', None))

        if appointment and request.user.role != 'admin':
            patient = getattr(request.user, 'patient', None)
            if not patient or appointment.patient_id != patient.id:
                raise serializers.ValidationError("Bu tashrifga baho qo'yish huquqingiz yo'q")

        if appointment and appointment.status != 'completed':
            raise serializers.ValidationError("Faqat yakunlangan tashrif uchun baho qoldirish mumkun")

        return attrs