from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SpecialityViewSet, RankTypeViewSet, RankPriceViewSet

router = DefaultRouter()
router.register(r'specialities', SpecialityViewSet)
router.register(r'ranktyp', RankTypeViewSet)
router.register(r'rankprice', RankPriceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
