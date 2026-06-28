from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MedicalCenterViewSet, ClinicTypeViewSet, ClinicViewSet

router = DefaultRouter()
router.register(r'medicalcenter', MedicalCenterViewSet)
router.register(r'clinictype', ClinicTypeViewSet)
router.register(r'clinics', ClinicViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
