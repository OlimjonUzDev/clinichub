from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .models import Speciality, RankType, RankPrice
from .serializers import SpecialitySerializers, RankTypeSerializers, RankPriceSerializers
from users.permissions import IsAdminOrReadOnly

class CustomPagination(PageNumberPagination):
    """Ro'yxat javoblarini bir sahifada 6 tadan elementga bo'lib beradi."""

    page_size = 6

class SpecialityViewSet(viewsets.ModelViewSet):
    """Mutaxassisliklar ("Speciality") uchun CRUD API endpointlarini taqdim etadi.

    O'qish (list/retrieve) hammaga ochiq, yaratish/o'zgartirish/o'chirish
    faqat administratorlarga ruxsat etiladi ("IsAdminOrReadOnly").
    "name_uz" va "name_ru" maydonlari bo'yicha qidiruv qo'llab-quvvatlanadi.
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class RankTypeViewSet(viewsets.ModelViewSet):
    """Shifokor toifalari ("RankType") uchun CRUD API endpointlarini taqdim etadi.

    O'qish hammaga ochiq, yozish amallari faqat administratorlarga
    ruxsat etiladi ("IsAdminOrReadOnly"). "name_uz" va "name_ru"
    maydonlari bo'yicha qidiruv qo'llab-quvvatlanadi.
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = RankType.objects.all()
    serializer_class = RankTypeSerializers
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class RankPriceViewSet(viewsets.ModelViewSet):
    """Toifa narxlari ("RankPrice") uchun CRUD API endpointlarini taqdim etadi.

    O'qish hammaga ochiq, yozish amallari faqat administratorlarga
    ruxsat etiladi ("IsAdminOrReadOnly").
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = RankPrice.objects.all()
    serializer_class = RankPriceSerializers
