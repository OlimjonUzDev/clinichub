from django.db import models

from users.models import User
from catalog.models import Speciality, RankType
from clinics.models import Clinic

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    rank_type = models.ForeignKey(RankType, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=225, blank=True)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    weekday = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return str(self.doctor)




