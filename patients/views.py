from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializers
from .permissions import IsAdminOrDoctor, IsAdminOrOwnerPatient
from users.permissions import IsAdmin

class CustomPagination(PageNumberPagination):
    """Bemorlar ro'yxati uchun sahifalash sozlamalari (har sahifada 6 ta element)."""

    page_size = 6

class PatientViewSet(viewsets.ModelViewSet):
    """Bemorlar (``Patient``) uchun CRUD amallarini ta'minlaydigan ViewSet.

    Ro'yxatni faqat admin yoki doktor ko'ra oladi, yaratish/o'chirish faqat
    adminga ruxsat etiladi, qolgan amallar esa admin yoki obyekt egasiga
    ochiq. ``name_uz`` va ``name_ru`` maydonlari bo'yicha qidiruv qo'llab-
    quvvatlanadi.
    """

    queryset = Patient.objects.all()
    serializer_class = PatientSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

    def get_queryset(self):
        """Foydalanuvchi roliga qarab ko'rinadigan bemorlar ro'yxatini qaytaradi.

        Qaytaradi:
            QuerySet: Admin yoki doktor uchun barcha bemorlar, aks holda
            faqat so'rov yuborgan foydalanuvchiga tegishli bemor.
        """
        user = self.request.user
        if user.role in ('admin', 'doctor'):
            return Patient.objects.all()
        return Patient.objects.filter(user=user)

    def get_permissions(self):
        """Joriy amal (action) uchun kerakli ruxsat sinflarini tanlaydi.

        Qaytaradi:
            list: Amalga mos permission obyektlari ro'yxati - ``list`` uchun
            ``IsAdminOrDoctor``, ``create``/``destroy`` uchun ``IsAdmin``,
            qolganlari uchun ``IsAdminOrOwnerPatient``.
        """
        if self.action == 'list':
            return [IsAdminOrDoctor()]
        if self.action in ['create', 'destroy']:
            return [IsAdmin()]
        return [IsAdminOrOwnerPatient()]

    @action(detail=False, methods=['get', 'post', 'patch'])
    def me(self, request):
        """So'rov yuborgan foydalanuvchining o'z bemor profilini boshqaradi.

        GET so'rovida mavjud profilni qaytaradi, POST so'rovida yangi
        profil yaratadi (agar u hali mavjud bo'lmasa), PATCH so'rovida esa
        mavjud profilni qisman yangilaydi. ``user`` maydoni har doim
        so'rov yuborgan foydalanuvchiga o'rnatiladi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi (GET, POST yoki PATCH).

        Qaytaradi:
            Response: Bemor ma'lumotlari yoki xatolik xabari bilan javob.
        """
        patient = Patient.objects.filter(user=request.user).first()

        if request.method == 'GET':
            if not patient:
                return Response({'detail': 'Patient profili topilmadi'}, status=400)
            return Response(self.get_serializer(patient).data)

        if request.method == 'POST':
            if patient:
                return Response({'detail': 'Patient profili allaqachon mavjud'}, status=400)
            serializer = self.get_serializer(data=request.data)
            serializer.fields.pop('user', None)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        if not patient:
            return Response({'detail': 'Patient profili topilmadi'}, status=400)
        serializer = self.get_serializer(patient, data=request.data, partial=True)
        serializer.fields.pop('user', None)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

