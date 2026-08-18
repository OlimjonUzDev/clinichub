import random
from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, OTPCode
from .serializers import RegisterSerializers, UserSerializers, OTPRequestSerializers, OTPVerifySerializers
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from .permissions import IsAdmin
from notifications.services import send_sms


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


class UserListView(generics.ListAPIView):
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializers


class DashboardView(APIView):
    permission_classes = [IsAdmin]
    def get(self, request):
        from clinics.models import Clinic
        return Response({
            'total_doctors':              Doctor.objects.count(),
            'total_patients':             Patient.objects.count(),
            'total_appointments':         Appointment.objects.count(),
            'total_clinics':              Clinic.objects.count(),
            'upcoming_appointments':      Appointment.objects.filter(status='pending').count(),
            'ongoing_appointments':       Appointment.objects.filter(status='confirmed').count(),
            'completed_appointments':     Appointment.objects.filter(status='completed').count(),
            'cancelled_appointments':     Appointment.objects.filter(status='cancelled').count(),
        })

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'role': request.user.role,
        })


class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.SMS_OTP_ENABLED:
            return Response({"detail": "SMS orqali vaqtinchalik o'chirilgan"}, status=503)
        serializer = OTPRequestSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        recent_exists = OTPCode.objects.filter(
            phone_number=phone_number,
            created_at__gte=timezone.now() - timedelta(seconds=60),
        ).exists()
        if recent_exists:
            return Response(
                {'detail': "Iltimos, biroz kuting va qayta urinib ko'ring"},
                status=429,
            )

        code = f"{random.randint(0, 999999):06d}"
        OTPCode.objects.create(
            phone_number=phone_number,
            code=code,
            expires_at=timezone.now() + timedelta(minutes=5),
        )
        send_sms(phone_number, f"ClinicHub tasdiqlash kodi: {code}")
        return Response({'detail': 'Kod yuborildi'}, status=200)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not settings.SMS_OTP_ENABLED:
            return Response({"detail": "SMS orqali vaqtinchalik o'chirilgan"}, status=503)
        serializer = OTPVerifySerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        otp = OTPCode.objects.filter(
            phone_number=phone_number, is_used=False
        ).order_by('-created_at').first()

        if not otp or not otp.is_valid():
            return Response(
                {'detail': "Kod noto'g'ri yoki muddati o'tgan"}, status=400
            )

        if otp.code != code:
            otp.attempts += 1
            otp.save()
            return Response({'detail': "Kod noto'g'ri"}, status=400)

        otp.is_used = True
        otp.save()

        user = User.objects.filter(phone_number=phone_number, role='patient').first()
        created = False
        if not user:
            user = User.objects.create_user(
                username=phone_number,
                phone_number=phone_number,
                role='patient',
            )
            created = True

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'is_new_user': created,
        }, status=200)

