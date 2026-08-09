from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.utils import timezone

class UserManager(DjangoUserManager):
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return self.username

class OTPCode(models.Model):
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    def is_valid(self):
        return not self.is_used and self.attempts < 5 and timezone.now() < self.expires_at
