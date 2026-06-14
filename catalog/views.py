from rest_framework import viewsets

from .models import Speciality, RankType
from .serializers import SpecilatySerializers, RankTypeSerializers

class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecilatySerializers

class RankTypeViewSet(viewsets.ModelViewSet):
    queryset = RankType.objects.all()
    serializer_class = RankTypeSerializers

# Create your views here.
