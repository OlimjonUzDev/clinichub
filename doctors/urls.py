from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DoctorViewSet, DoctorScheduleViewSet

router = DefaultRouter()
router.register(r'doctor', DoctorViewSet)
router.register(r'doctorschedule', DoctorScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
