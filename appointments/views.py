import datetime
from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .models import Appointment, Rating
from .serializers import AppointmentSerializers, RatingSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsPatient
from .permissions import IsAdminOrOwnerAppointments, IsAdminOrOwnerRating

class CustomPagination(PageNumberPagination):
    """Ro'yxat endpointlari uchun bir sahifada 6 ta element ko'rsatadigan paginatsiya."""

    page_size = 6

class AppointmentViewSet(viewsets.ModelViewSet):
    """Tashriflarni (Appointment) ro'yxatlash, yaratish, ko'rish va boshqarish uchun viewset.

    Bemor faqat o'z profiliga tashrif yaratishi mumkin (patient maydoni
    avtomatik biriktiriladi), admin va tashrif egalari esa mavjud
    tashriflarni to'liq boshqara oladi. Ruxsatlar get_permissions() orqali,
    ko'rinadigan tashriflar esa get_queryset() orqali cheklanadi.
    """

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['patient__name_uz', 'patient__name_ru']

    def create(self, request, *args, **kwargs):
        """Yangi tashrif yaratadi; bemor foydalanuvchi uchun patient maydonini avtomatik biriktiradi.

        Parametrlar:
            request: kiruvchi so'rov, tashrif ma'lumotlarini o'z ichiga oladi.

        Qaytaradi:
            Response: yaratilgan tashrif ma'lumotlari va 201 statusi,
                yoki bemor profili topilmasa 400 statusi bilan xabar.
        """
        serializers = self.get_serializer(data=request.data)
        if request.user.role == 'patient':
            serializers.fields.pop('patient', None)
            patient = getattr(request.user, 'patient', None)
            if not patient:
                return Response({'detail': 'Avval bemor profilingizni yarating'}, status=400)

        serializers.is_valid(raise_exception=True)

        if request.user.role == 'patient':
            serializers.save(patient=patient)
        else:
            serializers.save()

        headers = self.get_success_headers(serializers.data)
        return Response(serializers.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        """Admin uchun barcha tashriflarni, boshqalar uchun faqat o'ziga tegishlilarini qaytaradi.

        Qaytaradi:
            QuerySet: joriy foydalanuvchi ko'rishi mumkin bo'lgan tashriflar.
        """
        user = self.request.user
        if user.role == 'admin':
            return Appointment.objects.all()
        return Appointment.objects.filter(Q(patient__user=user) | Q(doctor__user=user))

    def get_permissions(self):
        """list/create amallari uchun IsAuthenticated, qolganlari uchun egalik tekshiruvini qaytaradi.

        Qaytaradi:
            list: joriy action uchun qo'llaniladigan permission obyektlari.
        """
        if self.action in ['list', 'create']:
            return [IsAuthenticated()]
        return [IsAdminOrOwnerAppointments()]

class RatingViewSet(viewsets.ModelViewSet):
    """Tashriflarga qoldirilgan baholarni (Rating) boshqarish uchun viewset.

    Yaratishda patient va doctor maydonlari tashrifdan avtomatik
    olinadi. Ruxsatlar amalga (list/retrieve/create/boshqa) qarab
    get_permissions() orqali farqlanadi.
    """

    queryset = Rating.objects.all()
    serializer_class = RatingSerializers

    def create(self, request, *args, **kwargs):
        """Yangi baho yaratadi va patient/doctor maydonlarini tashrifdan avtomatik biriktiradi.

        Parametrlar:
            request: kiruvchi so'rov, baho ma'lumotlarini o'z ichiga oladi.

        Qaytaradi:
            Response: yaratilgan baho ma'lumotlari va 201 statusi.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.validated_data['appointment']
        serializer.save(patient=appointment.patient, doctor=appointment.doctor)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        """Admin uchun barcha baholarni, boshqalar uchun faqat o'ziga tegishlilarini qaytaradi.

        Qaytaradi:
            QuerySet: joriy foydalanuvchi ko'rishi mumkin bo'lgan baholar.
        """
        user = self.request.user
        if user.role == 'admin':
            return Rating.objects.all()
        return Rating.objects.filter(Q(patient__user=user) | Q(doctor__user=user))

    def get_permissions(self):
        """Amalga qarab (list/retrieve, create, boshqa) tegishli permissionlarni qaytaradi.

        Qaytaradi:
            list: joriy action uchun qo'llaniladigan permission obyektlari.
        """
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsPatient()]
        return [IsAdminOrOwnerRating()]

class DoctorBusySlotsView(APIView):
    """Berilgan doktor va sanadagi band vaqt oralig'larini qaytaradi.
    Bemor kim ekanligi (appointment egasi) chiqarilmaydi — faqat vaqt oralig'i,
    shuning uchun boshqa bemorlarning maxfiyligi buzilmaydi."""
    permission_classes = [AllowAny]

    def get(self, request):
        """Berilgan doktor va sana bo'yicha band vaqt oralig'lari ro'yxatini qaytaradi.

        Parametrlar:
            request: 'doctor' va 'date' (YYYY-MM-DD) query parametrlarini
                o'z ichiga olgan so'rov.

        Qaytaradi:
            Response: band start_time/end_time juftliklari ro'yxati,
                yoki parametrlar noto'g'ri/yo'q bo'lsa 400 statusi bilan xabar.
        """
        doctor_id = request.query_params.get('doctor')
        date_str = request.query_params.get('date')
        if not doctor_id or not date_str:
            return Response({'detail': "'doctor' va 'date' parametrlari talab qilinadi"}, status=400)
        try:
            datetime.date.fromisoformat(date_str)
        except ValueError:
            return Response({'detail': "'date' formati noto'g'ri (YYYY-MM-DD)"}, status=400)

        qs = Appointment.objects.filter(
            doctor_id=doctor_id,
            start_time__date=date_str,
        ).exclude(status='cancelled').values('start_time', 'end_time')

        return Response(list(qs))

