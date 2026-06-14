from django.db import models

class Clinic(models.Model):
    name = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    phone_number = models.CharField(max_length=225)

# Create your models here.
