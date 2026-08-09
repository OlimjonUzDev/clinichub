from rest_framework import permissions

class IsAdminOrOwnerDoctor(permissions.BasePermission):
    """O'qish uchun ochiq, o'zgartirish uchun faqat admin yoki profil egasiga ruxsat beradi.

    Xavfsiz metodlar (GET, HEAD, OPTIONS) har doim ruxsat etiladi. Yozish
    metodlari uchun avval foydalanuvchi autentifikatsiyadan o'tgan bo'lishi,
    so'ng esa u admin yoki tegishli ``Doctor`` obyektining egasi bo'lishi
    talab qilinadi.
    """

    def has_permission(self, request, view):
        """Xavfsiz metodlarga yoki autentifikatsiyadan o'tgan foydalanuvchilarga ruxsat beradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ushbu ruxsat tekshirilayotgan view.

        Qaytaradi:
            bool: Amalni bajarishga ruxsat berilgan-bermagani.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


    def has_object_permission(self, request, view, obj):
        """Obyektni faqat admin yoki uning egasi o'zgartira olishini tekshiradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ushbu ruxsat tekshirilayotgan view.
            obj: Tekshirilayotgan ``Doctor`` obyekti.

        Qaytaradi:
            bool: Amalni bajarishga ruxsat berilgan-bermagani.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or obj.user == request.user

class IsAdminOrOwnerSchedule(permissions.BasePermission):
    """Jadval yozuvlariga kirishni admin, shifokor va boshqa foydalanuvchilar uchun cheklaydi.

    O'qish faqat autentifikatsiyadan o'tgan foydalanuvchilarga, yaratish
    (POST) faqat admin yoki shifokor rolidagilarga, obyektni o'zgartirish
    esa admin yoki tegishli jadval shifokoriga ruxsat etiladi.
    """

    def has_permission(self, request, view):
        """So'rov turiga qarab autentifikatsiya va rol talablarini tekshiradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ushbu ruxsat tekshirilayotgan view.

        Qaytaradi:
            bool: Amalni bajarishga ruxsat berilgan-bermagani.
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        if not request.user.is_authenticated:
            return False
        if request.method == 'POST':
            return request.user.role in ('admin', 'doctor')
        return True

    def has_object_permission(self, request, view, obj):
        """Jadval yozuvini faqat admin yoki uning shifokor-egasi o'zgartira olishini tekshiradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ushbu ruxsat tekshirilayotgan view.
            obj: Tekshirilayotgan ``DoctorSchedule`` obyekti.

        Qaytaradi:
            bool: Amalni bajarishga ruxsat berilgan-bermagani.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or obj.doctor.user == request.user
