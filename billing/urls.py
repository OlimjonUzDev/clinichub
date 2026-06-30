from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, DoctorPayoutViewSet

router = DefaultRouter()
router.register(r'invoice', InvoiceViewSet)
router.register(r'doctorpayout', DoctorPayoutViewSet)

urlpatterns = [
    path('', include(router.urls))
]
