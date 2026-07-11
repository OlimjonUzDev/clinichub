from rest_framework import serializers
from django.utils import timezone

from .models import Appointment, Rating
from doctors.models import DoctorSchedule

class AppointmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

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

class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'