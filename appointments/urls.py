from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AppointmentViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'appointment', AppointmentViewSet)
router.register(r'rating', RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
