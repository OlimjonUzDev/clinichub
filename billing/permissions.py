from rest_framework import permissions

class IsAdminOrOwnerInvoice(permissions.BasePermission):
    """Invoice obyektiga faqat admin yoki uning egasi bo'lgan bemorga ruxsat beradi.

    Admin barcha amallarni (o'qish va o'zgartirish) bajara oladi. Hisob-faktura
    egasi bo'lgan bemor esa faqat SAFE_METHODS (GET, HEAD, OPTIONS) orqali
    o'z hisob-fakturasini ko'ra oladi, o'zgartira olmaydi.
    """
    def has_permission(self, request, view):
        """Foydalanuvchi autentifikatsiyadan o'tganligini tekshiradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.

        Qaytaradi:
            bool: foydalanuvchi tizimga kirgan bo'lsa True.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Obyekt darajasidagi ruxsatni tekshiradi: admin yoki hisob-faktura egasi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.
            obj: tekshirilayotgan Invoice obyekti.

        Qaytaradi:
            bool: admin bo'lsa yoki egasi faqat o'qish so'rovini yuborsa True.
        """
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.patient.user == request.user
        return False

class IsAdminOrOwnerPayout(permissions.BasePermission):
    """DoctorPayout obyektiga faqat admin yoki uning egasi bo'lgan shifokorga ruxsat beradi.

    Admin barcha amallarni (o'qish va o'zgartirish) bajara oladi. To'lov
    egasi bo'lgan shifokor esa faqat SAFE_METHODS (GET, HEAD, OPTIONS) orqali
    o'z to'lovini ko'ra oladi, o'zgartira olmaydi.
    """
    def has_permission(self, request, view):
        """Foydalanuvchi autentifikatsiyadan o'tganligini tekshiradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.

        Qaytaradi:
            bool: foydalanuvchi tizimga kirgan bo'lsa True.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Obyekt darajasidagi ruxsatni tekshiradi: admin yoki to'lov egasi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view.
            obj: tekshirilayotgan DoctorPayout obyekti.

        Qaytaradi:
            bool: admin bo'lsa yoki egasi faqat o'qish so'rovini yuborsa True.
        """
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.doctor.user == request.user
        return False
    
    