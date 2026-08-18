import datetime

from rest_framework.views import APIView
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from django.db.models import Q
from django.db import transaction

from .models import Appointment, Rating
from .serializers import AppointmentSerializers, RatingSerializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.permissions import IsPatient
from .permissions import IsAdminOrOwnerAppointments, IsAdminOrOwnerRating
from doctors.models import Doctor

class CustomPagination(PageNumberPagination):
    page_size = 6

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['patient__name_uz', 'patient__name_ru']

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        patient = None

        if request.user.role == 'patient':
            patient = getattr(request.user, 'patient', None)
            if not patient:
                return Response({'detail': 'Avval bemor profilingizni yarating'}, status=400)

        if request.user.role == 'doctor':
            doctor = getattr(request.user, 'doctor', None)
            if not doctor:
                return Response({'detail': 'Avval doctor profilingizni yarating'}, status=400)
            data['doctor'] = doctor.id

        doctor_id = data.get('doctor')

        with transaction.atomic():
            if doctor_id:
                # Shu shifokor uchun boshqa bron urinishlari shu qatorni bo'shatishini kutadi —
                # shu bilan overlap tekshiruvi va yozish orasidagi "teshik" yopiladi.
                Doctor.objects.select_for_update().filter(pk=doctor_id).first()

            serializers = self.get_serializer(data=data)
            if request.user.role == 'patient':
                serializers.fields.pop('patient', None)

            serializers.is_valid(raise_exception=True)

            if patient:
                serializers.save(patient=patient)
            else:
                serializers.save()

        headers = self.get_success_headers(serializers.data)
        return Response(serializers.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()  # IsAdminOrOwnerAppointments avtomatik tekshiradi
        if request.user.role not in ('admin', 'doctor') or appointment.doctor.user != request.user and request.user.role != 'admin':
            return Response({'detail': "Faqat shifokor yoki admin tasdiqlashi mumkin"}, status=403)
        if appointment.status != 'pending':
            return Response({'detail': "Faqat 'pending' holatidagi tashrif tasdiqlanadi"}, status=400)
        appointment.status = 'confirmed'
        appointment.save()
        return Response(self.get_serializer(appointment).data)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        if request.user.role not in ('admin', 'doctor') or appointment.doctor.user != request.user and request.user.role != 'admin':
            return Response({'detail': "Faqat shifokor yoki admin yakunlashi mumkin"}, status=403)
        if appointment.status != 'confirmed':
            return Response({'detail': "Faqat 'confirmed' holatidagi tashrif yakunlanadi"}, status=400)
        appointment.status = 'completed'
        appointment.save()
        return Response(self.get_serializer(appointment).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()  # patient/doctor/admin — o'ziniki bo'lsa ruxsat bor
        if appointment.status in ('completed', 'cancelled'):
            return Response({'detail': "Bu tashrif allaqachon yakunlangan yoki bekor qilingan"}, status=400)
        appointment.status = 'cancelled'
        appointment.cancelled_by = request.user
        appointment.cancel_reason = request.data.get('cancel_reason', '')
        appointment.save()
        return Response(self.get_serializer(appointment).data)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Appointment.objects.all()
        return Appointment.objects.filter(Q(patient__user=user) | Q(doctor__user=user))

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAuthenticated()]
        return [IsAdminOrOwnerAppointments()]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.validated_data['appointment']
        serializer.save(patient=appointment.patient, doctor=appointment.doctor)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Rating.objects.all()
        return Rating.objects.filter(Q(patient__user=user) | Q(doctor__user=user))

    def get_permissions(self):
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

