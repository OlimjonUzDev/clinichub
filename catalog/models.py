from django.db import models

class Speciality(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class RankType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class RankPrice(models.Model):
    CONSULTATION_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline')
    )
    rannk_type = models.ForeignKey(RankType, on_delete=models.CASCADE)
    consultation_type = models.CharField(max_length=225, choices=CONSULTATION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
