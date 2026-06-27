from django.db import models

from users.models import User
from catalog.models import Speciality, RankType
from clinics.models import Clinic

class Doctor(models.Model):
    GENDER_CHOICES = (
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    rank_type = models.ForeignKey(RankType, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=225, blank=True)
    name_uz = models.CharField(max_length=225)
    name_ru = models.CharField(max_length=225)
    bio_uz = models.TextField(blank=True)
    bio_ru = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    avatar = models.URLField(blank=True)
    gender = models.CharField(max_length=225, choices=GENDER_CHOICES, default='erkak', blank=True)

    def __str__(self):
        return self.user.username

class DoctorSchedule(models.Model):
    WEEKDAY_CHOICES = (
        (0, 'Dushanba'),
        (1, 'Seshanba'),
        (2, 'Chorshanba'),
        (3, 'Payshanba'),
        (4, 'Juma'),
        (5, 'Shanba'),
        (6, 'Yakshanba')
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    weekday = models.PositiveSmallIntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'weekday')

    def __str__(self):
        return str(self.doctor)




