from rest_framework import permissions

class IsAdminOrOwnerPrescription(permissions.BasePermission):
    """Retseptga faqat admin, uning shifokori yoki bemori kirishi mumkinligini ta'minlaydi.

    O'qish (SAFE_METHODS) uchun shifokor yoki bemorning o'ziga ruxsat beriladi,
    yozish (create/update/delete) uchun esa faqat tegishli shifokorga ruxsat beriladi.
    """

    def has_permission(self, request, view):
        """Faqat autentifikatsiyadan o'tgan foydalanuvchilarga ruxsat beradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view obyekti.

        Qaytaradi:
            bool: foydalanuvchi autentifikatsiyadan o'tgan bo'lsa True.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Berilgan retsept obyektiga ruxsatni tekshiradi.

        Admin uchun har doim ruxsat beriladi. O'qish so'rovlari uchun retseptning
        shifokori yoki bemori bo'lish yetarli, o'zgartirish so'rovlari uchun esa
        faqat retseptning shifokori bo'lish talab qilinadi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view obyekti.
            obj: tekshirilayotgan Prescription obyekti.

        Qaytaradi:
            bool: foydalanuvchiga ushbu obyekt ustida amal bajarishga ruxsat bor-yo'qligi.
        """
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.doctor.user == request.user or obj.patient.user == request.user
        return obj.doctor.user == request.user

class IsAdminOrOwnerPrescriptionItem(permissions.BasePermission):
    """Retsept bandiga (item) faqat admin, tegishli shifokor yoki bemor kirishi mumkinligini ta'minlaydi.

    Ruxsat mantig'i IsAdminOrOwnerPrescription bilan bir xil, faqat egalik
    tekshiruvi item.prescription orqali bog'liq shifokor/bemorga qarab amalga oshiriladi.
    """

    def has_permission(self, request, view):
        """Faqat autentifikatsiyadan o'tgan foydalanuvchilarga ruxsat beradi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view obyekti.

        Qaytaradi:
            bool: foydalanuvchi autentifikatsiyadan o'tgan bo'lsa True.
        """
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Berilgan retsept bandi obyektiga ruxsatni tekshiradi.

        Admin uchun har doim ruxsat beriladi. O'qish so'rovlari uchun bandning
        tegishli bo'lgan retseptidagi shifokor yoki bemor bo'lish yetarli,
        o'zgartirish so'rovlari uchun esa faqat retseptning shifokori bo'lish talab qilinadi.

        Parametrlar:
            request: joriy so'rov obyekti.
            view: chaqirilayotgan view obyekti.
            obj: tekshirilayotgan PrescriptionItem obyekti.

        Qaytaradi:
            bool: foydalanuvchiga ushbu obyekt ustida amal bajarishga ruxsat bor-yo'qligi.
        """
        if request.user.role == 'admin':
            return True
        if request.method in permissions.SAFE_METHODS:
            return obj.prescription.doctor.user == request.user or obj.prescription.patient.user == request.user
        return obj.prescription.doctor.user == request.user
