from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Speciality, RankType, RankPrice
from .serializers import SpecialitySerializers, RankTypeSerializers, RankPriceSerializers
from users.permissions import IsAdminOrReadOnly

class CustomPagination(PageNumberPagination):
    page_size = 6

class SpecialityViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class RankTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = RankType.objects.all()
    serializer_class = RankTypeSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class RankPriceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = RankPrice.objects.all()
    serializer_class = RankPriceSerializers
