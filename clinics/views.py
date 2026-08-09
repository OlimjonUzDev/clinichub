from rest_framework import viewsets, filters
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination

from .models import MedicalCenter, ClinicType, Clinic
from .serializers import MedicalCenterSerializers, ClinicTypeSerializers, ClinicSerializers
from users.permissions import IsAdminOrReadOnly

class CustomPagination(PageNumberPagination):
    """Sahifa hajmi 6 taga teng bo'lgan standart sahifalash sozlamasi."""

    page_size = 6

class MedicalCenterViewSet(viewsets.ModelViewSet):
    """Tibbiyot markazlari (``MedicalCenter``) uchun CRUD endpointi.

    O'qish (list/retrieve) hamma uchun ochiq, yozish (create/update/delete)
    faqat administratorlarga ruxsat etilgan (``IsAdminOrReadOnly``).
    ``name_uz`` va ``name_ru`` maydonlari bo'yicha qidiruv qo'llab-quvvatlanadi.
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = MedicalCenter.objects.all()
    serializer_class = MedicalCenterSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

class ClinicTypeViewSet(viewsets.ModelViewSet):
    """Klinika turlari (``ClinicType``) uchun CRUD endpointi.

    O'qish hamma uchun ochiq, yozish faqat administratorlarga ruxsat
    etilgan (``IsAdminOrReadOnly``).
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = ClinicType.objects.all()
    serializer_class = ClinicTypeSerializers

class ClinicViewSet(viewsets.ModelViewSet):
    """Klinikalar (``Clinic``) uchun CRUD endpointi.

    O'qish hamma uchun ochiq, yozish faqat administratorlarga ruxsat
    etilgan (``IsAdminOrReadOnly``). Tibbiyot markazi nomi bo'yicha
    qidiruv qo'llab-quvvatlanadi.
    """

    permission_classes = [IsAdminOrReadOnly]
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['medical_center__name_uz', 'medical_center__name_ru']

    def get_queryset(self):
        """Har bir klinika uchun bog'liq shifokorlar sonini hisoblab qo'shadi.

        Qaytaradi:
            QuerySet: ``doctors_count`` annotatsiyasi bilan boyitilgan
            ``Clinic`` obyektlari ro'yxati.
        """

        return Clinic.objects.annotate(doctors_count=Count('doctor'))


# Create your views here.
