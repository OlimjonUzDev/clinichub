from django.contrib import admin

from .models import Speciality, RankType, RankPrice

admin.site.register(Speciality)
admin.site.register(RankType)
admin.site.register(RankPrice)

# Register your models here.
