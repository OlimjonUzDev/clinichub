from django.contrib import admin

from .models import MedicalCenter, ClinicType, Clinic

admin.site.register(MedicalCenter)
admin.site.register(ClinicType)
admin.site.register(Clinic)

