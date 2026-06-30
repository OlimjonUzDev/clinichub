from django.db import models
from clinics.models import Clinic

class Speciality(models.Model):
    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name_uz

class RankType(models.Model):
    name_uz = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_uz

class RankPrice(models.Model):
    rank_type = models.ForeignKey(RankType, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=225, default='UZS')
    duration_min = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
