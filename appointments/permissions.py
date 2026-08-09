from rest_framework import permissions

class IsAdminOrOwnerAppointments(permissions.BasePermission):
    """Tashrif (Appointment) obyektiga faqat admin, egasi bemor yoki egasi doktor kirisha oladi.

    Ro'yxatdan o'tgan har bir foydalanuvchi umumiy ruxsatga ega, ammo
    xavfsiz bo'lmagan (o'zgartiruvchi) amallar faqat admin, tashrifning
    bemori yoki doktori uchun ruxsat etiladi.
    """

    def has_permission(self, request, view):
        """Foydalanuvchi autentifikatsiyadan o'tgan bo'lsa ruxsat beradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.

        Qaytaradi:
            bool: foydalanuvchi tizimga kirgan bo'lsa True.
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Xavfsiz metodlarga hammaga, boshqalariga admin/egalariga ruxsat beradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.
            obj: tekshirilayotgan Appointment obyekti.

        Qaytaradi:
            bool: foydalanuvchi admin, tashrif bemori yoki doktori bo'lsa True.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or obj.patient.user == request.user or obj.doctor.user == request.user

class IsAdminOrOwnerRating(permissions.BasePermission):
    """Baho (Rating) obyektiga faqat admin yoki bahoni qoldirgan bemor kirisha oladi.

    O'qish (SAFE_METHODS) uchun hammaga ruxsat, o'zgartirish uchun esa
    faqat admin yoki bahoning egasi bo'lgan bemorga ruxsat beriladi.
    """

    def has_permission(self, request, view):
        """Xavfsiz metodlarga hammaga, aks holda faqat autentifikatsiyadan o'tganlarga ruxsat beradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.

        Qaytaradi:
            bool: ruxsat berilsa True.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Xavfsiz metodlarga hammaga, boshqalariga admin/bemor egasiga ruxsat beradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.
            obj: tekshirilayotgan Rating obyekti.

        Qaytaradi:
            bool: foydalanuvchi admin yoki bahoning bemori bo'lsa True.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'admin' or obj.patient.user == request.user