from rest_framework import permissions

class IsAdminOrOwnerPatient(permissions.BasePermission):
    """Faqat admin yoki bemor obyektining egasiga ruxsat beradi.

    So'rov darajasida foydalanuvchi autentifikatsiyadan o'tgan bo'lishi
    talab qilinadi, obyekt darajasida esa faqat ``admin`` roli yoki
    ``Patient.user`` maydoni so'rov yuborayotgan foydalanuvchiga teng
    bo'lgan holatlarga ruxsat beriladi.
    """

    def has_permission(self, request, view):
        """Foydalanuvchi autentifikatsiyadan o'tganligini tekshiradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ruxsat tekshirilayotgan view.

        Qaytaradi:
            bool: Foydalanuvchi mavjud va autentifikatsiyadan o'tgan bo'lsa ``True``.
        """
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Foydalanuvchi admin yoki obyekt egasi ekanligini tekshiradi.

        Parametrlar:
            request: Kiruvchi HTTP so'rovi.
            view: Ruxsat tekshirilayotgan view.
            obj: Tekshirilayotgan ``Patient`` obyekti.

        Qaytaradi:
            bool: Foydalanuvchi admin bo'lsa yoki obyektning egasi bo'lsa ``True``.
        """
        return request.user.role == 'admin' or obj.user == request.user

class IsAdminOrDoctor(permissions.BasePermission):
    """Faqat ``admin`` yoki ``doctor`` rolidagi foydalanuvchilarga ruxsat beradi."""

    def has_permission(self, request, view):
            """Foydalanuvchi autentifikatsiyadan o'tgan va roli admin yoki doctor ekanligini tekshiradi.

            Parametrlar:
                request: Kiruvchi HTTP so'rovi.
                view: Ruxsat tekshirilayotgan view.

            Qaytaradi:
                bool: Shartlar bajarilsa ``True``.
            """
            return request.user.is_authenticated and request.user.role in ('admin', 'doctor')