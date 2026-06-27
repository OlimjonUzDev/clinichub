from django.db import models
    
class MedicalCenter(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    name_uz = models.CharField(max_length=225)
    name_ru = models.CharField(max_length=225)
    contact = models.CharField(max_length=225, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    logo = models.URLField(blank=True)
    webiste = models.URLField(blank=True)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_uz

class ClinicType(models.Model):
    name_uz = models.CharField(max_length=225)
    name_ru = models.CharField(max_length=225)

    def __str__(self):
        return self.name_uz
    
class Clinic(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    medical_center = models.ForeignKey(MedicalCenter, on_delete=models.CASCADE)
    clinic_type = models.ForeignKey(ClinicType, on_delete=models.CASCADE)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='active')
    phone_number = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
