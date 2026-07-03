from rest_framework import viewsets, filters

from .models import Speciality, RankType, RankPrice
from .serializers import SpecialitySerializers, RankTypeSerializers, RankPriceSerializers
from users.permissions import IsAdmin

class SpecialityViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class RankTypeViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = RankType.objects.all()
    serializer_class = RankTypeSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class RankPriceViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = RankPrice.objects.all()
    serializer_class = RankPriceSerializers
