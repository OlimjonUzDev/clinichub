import random
from datetime import timedelta

from django.utils import timezone
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
    """Login/parol orqali yangi foydalanuvchi (patient) ro'yxatdan o'tkazish endpointi.

    Ruxsat: hammaga ochiq (AllowAny). Yaratish mantig'i RegisterSerializers
    ichida bo'lib, rolni har doim 'patient' qilib belgilaydi.
    """
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializers


class UserListView(generics.ListAPIView):
    """Barcha foydalanuvchilar ro'yxatini qaytaradi. Faqat adminlar uchun ruxsat etilgan."""
    permission_classes = [IsAdmin]
    queryset = User.objects.all()
    serializer_class = UserSerializers


class DashboardView(APIView):
    """Admin panel uchun umumiy statistika (doctors, patients, appointments, clinics) endpointi."""
    permission_classes = [IsAdmin]
    def get(self, request):
        """Doktorlar, bemorlar, klinikalar va uchrashuvlar bo'yicha umumiy sonlarni qaytaradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.

        Qaytaradi:
            Response: umumiy va holat bo'yicha (pending/confirmed/completed/
            cancelled) uchrashuvlar sonini o'z ichiga olgan JSON.
        """
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
    """Joriy autentifikatsiyadan o'tgan foydalanuvchining asosiy ma'lumotlarini qaytaradi."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """So'rov muallifining id, username va role maydonlarini qaytaradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi (request.user autentifikatsiyadan o'tgan bo'lishi shart).

        Qaytaradi:
            Response: foydalanuvchining id, username va role maydonlarini o'z ichiga olgan JSON.
        """
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'role': request.user.role,
        })


class RequestOTPView(APIView):
    """Telefon raqamiga bir martalik (OTP) kod yuboradi."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Telefon raqami uchun yangi OTP kod yaratadi va SMS orqali yuboradi.

        So'nggi 60 soniya ichida shu raqamga kod yuborilgan bo'lsa, so'rov
        429 (Too Many Requests) statusi bilan rad etiladi. Yangi kod 6 xonali
        tasodifiy son bo'lib, 5 daqiqa amal qiladi va notifications.services
        orqali SMS ko'rinishida yuboriladi.

        Parametrlar:
            request: 'phone_number' maydonini o'z ichiga olgan HTTP so'rovi.

        Qaytaradi:
            Response: muvaffaqiyatli bo'lsa 200 status va 'Kod yuborildi' xabari;
            juda tez-tez so'ralsa 429 status.
        """
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
    """OTP kodni tasdiqlaydi va JWT (access + refresh) qaytaradi.

    Mavjud (User.phone_number bo'yicha topilgan) patient uchun — kirish.
    Topilmasa — parolsiz yangi patient User yaratiladi (ro'yxatdan o'tish).
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Berilgan telefon raqami va kod bo'yicha eng so'nggi ishlatilmagan OTP'ni tasdiqlaydi.

        Kod topilmasa yoki muddati o'tgan/urinishlar limiti tugagan bo'lsa (is_valid())
        400 status qaytaradi. Kod noto'g'ri bo'lsa attempts sonini oshirib, 400 qaytaradi.
        To'g'ri bo'lsa, OTP is_used=True qilib belgilanadi, shu telefon raqamiga
        bog'langan 'patient' foydalanuvchi qidiriladi — topilmasa, parolsiz yangi
        patient User yaratiladi. Har ikki holatda ham SimpleJWT orqali
        access va refresh tokenlar generatsiya qilinadi.

        Parametrlar:
            request: 'phone_number' va 'code' maydonlarini o'z ichiga olgan HTTP so'rovi.

        Qaytaradi:
            Response: muvaffaqiyatli bo'lsa 200 status bilan 'access', 'refresh'
            tokenlar va 'is_new_user' bayrog'i; kod noto'g'ri/eskirgan bo'lsa 400 status.
        """
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

