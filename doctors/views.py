from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Doctor, DoctorSchedule
from .serializers import DoctorSerializers, DoctorScheduleSerializers
from .permissions import IsAdminOrOwnerDoctor, IsAdminOrOwnerSchedule
from users.permissions import IsAdminOrReadOnly

class CustomPagination(PageNumberPagination):
    """Ro'yxat javoblarini har sahifada 6 tadan elementga bo'lib beradi."""

    page_size = 6

class DoctorViewSet(viewsets.ModelViewSet):
    """Shifokorlar ustida CRUD amallarini bajaruvchi endpoint.

    Ro'yxat va bitta obyektni ko'rish, shuningdek yaratish/o'chirish faqat
    admin uchun ochiq (``IsAdminOrReadOnly``), qolgan amallar (masalan,
    yangilash) esa admin yoki profil egasiga ruxsat etiladi
    (``IsAdminOrOwnerDoctor``). ``name_uz`` va ``name_ru`` maydonlari
    bo'yicha qidiruv qo'llab-quvvatlanadi.
    """

    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

    def get_permissions(self):
        """Joriy amalga (action) qarab kerakli ruxsat klasslarini tanlaydi.

        Qaytaradi:
            list: Joriy so'rov uchun qo'llaniladigan permission obyektlari ro'yxati.
        """
        if self.action in ['list', 'retrieve']:
            return [IsAdminOrReadOnly()]
        if self.action in ['create', 'destroy']:
            return [IsAdminOrReadOnly()]
        return [IsAdminOrOwnerDoctor()]


class DoctorScheduleViewSet(viewsets.ModelViewSet):
    """Shifokorlarning ish jadvali (``DoctorSchedule``) ustida CRUD amallarini bajaruvchi endpoint.

    Kirish huquqi ``IsAdminOrOwnerSchedule`` orqali admin va tegishli
    shifokor bilan cheklanadi.
    """

    permission_classes = [IsAdminOrOwnerSchedule]
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializers

    def create(self, request, *args, **kwargs):
        """Yangi jadval yozuvini yaratadi, shifokor rolidagi foydalanuvchi uchun cheklovlarni qo'llaydi.

        Agar so'rovni yuborayotgan foydalanuvchi 'doctor' rolida bo'lsa,
        ``doctor`` maydoni kiritish uchun yashiriladi va avtomatik ravishda
        uning o'ziga bog'lanadi; shifokor profili mavjud emasligi yoki shu
        hafta kuni uchun jadval allaqachon mavjudligi tekshiriladi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            *args: Qo'shimcha pozitsion argumentlar.
            **kwargs: Qo'shimcha nomlangan argumentlar.

        Qaytaradi:
            Response: Yaratilgan jadval ma'lumotlari (201) yoki xatolik haqida javob (400).
        """
        serializers = self.get_serializer(data=request.data)
        if request.user.role == 'doctor':
            serializers.fields.pop('doctor', None)
            doctor = getattr(request.user, 'doctor', None)
            if not doctor:
                return Response({'detail': 'Avval doctor profilingizni yarating'}, status=400)
            if DoctorSchedule.objects.filter(doctor=doctor, weekday=request.data.get('weekday')).exists():
                return Response({'detail': 'Bu kun uchun jadval allaqachon mavjud'}, status=400)
            
        serializers.is_valid(raise_exception=True)

        if request.user.role == 'doctor':
            serializers.save(doctor=doctor)
        else:
            serializers.save()

        headers = self.get_success_headers(serializers.data)
        return Response(serializers.data, status=status.HTTP_201_CREATED, headers=headers)

