from django.db import models
    
class MedicalCenter(models.Model):
    """Tibbiyot markazini ifodalaydi.

    O'zbek va rus tillaridagi nomi, aloqa ma'lumotlari, manzili, logotipi
    va veb-sayti kabi maydonlarni, shuningdek ``status`` (active/inactive)
    holatini saqlaydi.
    """

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
    website = models.URLField(blank=True)
    status = models.CharField(max_length=225, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name_uz

class ClinicType(models.Model):
    """Klinika turini (masalan, poliklinika, stomatologiya) ifodalaydi.

    O'zbek va rus tillaridagi nomini saqlaydi.
    """

    name_uz = models.CharField(max_length=225)
    name_ru = models.CharField(max_length=225)

    def __str__(self):
        return self.name_uz
    
class Clinic(models.Model):
    """Muayyan tibbiyot markaziga tegishli klinikani ifodalaydi.

    ``medical_center`` va ``clinic_type`` bilan bog'liq (ForeignKey,
    ``on_delete=CASCADE``), telefon raqami va ``status`` (active/inactive)
    holatini saqlaydi.
    """

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
        return f"{self.clinic_type} - {self.medical_center}"
