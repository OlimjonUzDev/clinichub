from rest_framework import viewsets

from .models import Speciality, RankType, RankPrice
from .serializers import SpecilatySerializers, RankTypeSerializers, RankPriceSerializers

class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecilatySerializers

class RankTypeViewSet(viewsets.ModelViewSet):
    queryset = RankType.objects.all()
    serializer_class = RankTypeSerializers

class RankPriceViewSet(viewsets.ModelViewSet):
    queryset = RankPrice.objects.all()
    serializer_class = RankPriceSerializers
