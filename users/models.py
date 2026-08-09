from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.utils import timezone

class UserManager(DjangoUserManager):
    """Standart Django UserManager'ni superuser yaratishda 'admin' rolini qo'yadigan qilib kengaytiradi."""

    def create_superuser(self, username, email, password, **extra_fields):
        """Superfoydalanuvchi yaratadi va unga avtomatik 'admin' rolini beradi.

        Parametrlar:
            username: Foydalanuvchi nomi.
            email: Elektron pochta manzili.
            password: Parol.
            extra_fields: Modelga uzatiladigan qo'shimcha maydonlar.

        Qaytaradi:
            Yaratilgan superfoydalanuvchi (User) obyekti.
        """
        extra_fields.setdefault('role', 'admin')
        return super().create_superuser(username, email, password, **extra_fields)

class User(AbstractUser):
    """Tizimning asosiy foydalanuvchi modeli (Django AbstractUser'ga asoslangan).

    'role' maydoni orqali admin, doctor yoki patient rollarini belgilaydi.
    Qo'shimcha maydonlar: telefon raqami, avatar URL manzili va yaratilgan sana.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    phone_number = models.CharField(max_length=20, blank=True)
    avatar = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()

    def __str__(self):
        return self.username

class OTPCode(models.Model):
    """Telefon raqamiga yuborilgan bir martalik (OTP) tasdiqlash kodini saqlaydi.

    Kod yaratilgan vaqti, amal qilish muddati (expires_at), ishlatilganlik
    holati (is_used) va noto'g'ri urinishlar soni (attempts) kuzatiladi.
    """
    phone_number = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    def is_valid(self):
        """Kod hali ishlatilmagan, urinishlar soni 5 dan kam va muddati o'tmaganligini tekshiradi.

        Qaytaradi:
            Kod amal qiladigan bo'lsa True, aks holda False.
        """
        return not self.is_used and self.attempts < 5 and timezone.now() < self.expires_at
