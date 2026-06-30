from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PrescriptionViewSet, PrescriptionItemViewSet

router = DefaultRouter()
router.register(r'prescription', PrescriptionViewSet, basename='prescription')
router.register(r'prescription-item', PrescriptionItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
