from django.db import models
from clinics.models import Clinic

class Speciality(models.Model):
    """Shifokorlik mutaxassisligini (masalan, terapevt, kardiolog) ifodalaydi.

    O'zbek va rus tillaridagi nomlarini ("name_uz", "name_ru") saqlaydi.
    """

    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)


    def __str__(self):
        return self.name_uz

class RankType(models.Model):
    """Shifokor toifasini/darajasini (masalan, oliy, birinchi) ifodalaydi.

    O'zbek va rus tillaridagi nomlari hamda yaratilgan sanasini saqlaydi.
    """

    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_uz

class RankPrice(models.Model):
    """Klinikada shifokor toifasi bo'yicha konsultatsiya narxini ifodalaydi.

    Har bir "rank_type" va "clinic" birikmasi uchun narx, valyuta,
    davomiylik va konsultatsiya turini ("video", "voice", "chat",
    "in_person") belgilaydi.
    """

    CONSULTATION_CHOICES = (
        ('video', 'Video'),
        ('voice', 'Voice'),
        ('chat', 'Chat'),
        ('in_person', 'In-person'),
    )
    rank_type = models.ForeignKey(RankType, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=225, default='UZS')
    duration_min = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    consultation_type = models.CharField(max_length=225, choices=CONSULTATION_CHOICES, default='in_person')
