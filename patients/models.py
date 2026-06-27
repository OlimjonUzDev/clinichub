from django.db import models
from users.models import User

class Patient(models.Model):
    GENDER_CHOICE = (
        ('erkak', 'Erkak'),
        ('ayol', 'Ayol')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=225)
    name_ru = models.CharField(max_length=225)
    gender = models.CharField(max_length=225, choices=GENDER_CHOICE, default='erkak', blank=True)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=225, blank=True)
    address = models.CharField(max_length=225, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

