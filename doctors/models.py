from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator

from users.models import User
from catalog.models import Speciality, RankType
from clinics.models import Clinic

name_validator = RegexValidator(
    regex=r"^[A-Za-zА-Яа-яЁёʻʼ'\-\s]+$",
    message="Ism faqat harflardan iborat bo'lishi kerak.",
)
telegram_validator = RegexValidator(
    regex=r"^@?[A-Za-z0-9_]{5,32}$",
    message="Telegram username noto'g'ri formatda.",
)

class Doctor(models.Model):
    GENDER_CHOICES = (
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    rank_type = models.ForeignKey(RankType, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=225, blank=True, validators=[telegram_validator])
    name_uz = models.CharField(max_length=225, validators=[name_validator])
    name_ru = models.CharField(max_length=225, validators=[name_validator])
    bio_uz = models.TextField(blank=True)
    bio_ru = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    avatar = models.URLField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='erkak', blank=True)
    is_active = models.BooleanField(default=True)
    bank_name = models.CharField(max_length=225, blank=True)
    iban = models.CharField(max_length=34, blank=True)
    revenue_percentage = models.DecimalField(max_digits=3, decimal_places=2, default=1.00,validators=[MinValueValidator(0), MaxValueValidator(1)],)
    auto_payout = models.BooleanField(default=False)

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




