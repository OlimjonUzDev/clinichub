from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Faqat autentifikatsiyadan o'tgan va 'admin' roliga ega foydalanuvchilarga ruxsat beradi."""

    def has_permission(self, request, view):
        """So'rov muallifi autentifikatsiyadan o'tgan va roli 'admin' ekanligini tekshiradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ushbu ruxsat tekshirilayotgan view obyekti.

        Qaytaradi:
            Foydalanuvchi admin bo'lsa True, aks holda False.
        """
        return request.user.is_authenticated and request.user.role == 'admin'

class IsAdminOrReadOnly(permissions.BasePermission):
    """O'qish (SAFE_METHODS) uchun hammaga, o'zgartirish uchun faqat adminlarga ruxsat beradi."""

    def has_permission(self, request, view):
        """So'rov xavfsiz metod bo'lsa ruxsat beradi, aks holda faqat admin uchun ruxsat beradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ushbu ruxsat tekshirilayotgan view obyekti.

        Qaytaradi:
            Xavfsiz metod (GET/HEAD/OPTIONS) uchun True; aks holda foydalanuvchi
            admin bo'lgandagina True.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'

class IsPatient(permissions.BasePermission):
    """Faqat autentifikatsiyadan o'tgan va 'patient' roliga ega foydalanuvchilarga ruxsat beradi."""

    def has_permission(self, request, view):
        """So'rov muallifi autentifikatsiyadan o'tgan va roli 'patient' ekanligini tekshiradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ushbu ruxsat tekshirilayotgan view obyekti.

        Qaytaradi:
            Foydalanuvchi patient bo'lsa True, aks holda False.
        """
        return request.user.is_authenticated and request.user.role == 'patient'
        

