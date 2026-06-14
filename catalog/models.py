from django.db import models

class Speciality(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

class RankType(models.Model):
    name = models.CharField(max_length=50)
