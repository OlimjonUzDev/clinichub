from django.db import models
from users.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    address = models.CharField(max_length=225, blank=True)
    
    def __str__(self):
        return self.user.username

