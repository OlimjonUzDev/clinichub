from django.db import models
from django.core.validators import RegexValidator

from users.models import User

name_validator = RegexValidator(
    regex=r"^[A-Za-zА-Яа-яЁёʻʼ'\-\s]+$",
    message="Ism faqat harflardan iborat bo'lishi kerak.",
)
phone_validator = RegexValidator(
    regex=r"^\+998\d{9}$",
    message="Telefon raqam +998XXXXXXXXX formatida bo'lishi kerak.",
)

national_id_validator = RegexValidator(
    regex=r"^\d{14}$",
    message="JSHSHIR 14 xonali raqamdan iborat bo'lishi kerak.",
)

class Patient(models.Model):
    GENDER_CHOICE = (
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=225, validators=[name_validator])
    name_ru = models.CharField(max_length=225, validators=[name_validator])
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, default='erkak', blank=True)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=225, blank=True, validators=[phone_validator])
    national_id  = models.CharField(max_length=20, blank=True, validators=[national_id_validator])
    address      = models.CharField(max_length=225, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

