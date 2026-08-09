from rest_framework import viewsets

from .models import Invoice, DoctorPayout
from .serializers import InvoiceSerializers, DoctorPayoutSerializers
from users.permissions import IsAdmin
from .permissions import IsAdminOrOwnerInvoice, IsAdminOrOwnerPayout

class InvoiceViewSet(viewsets.ModelViewSet):
    """Hisob-fakturalar (Invoice) uchun CRUD amallarini taqdim etuvchi ViewSet.

    Faqat admin yangi hisob-faktura yarata oladi ('create' amali uchun IsAdmin
    talab qilinadi). Boshqa amallar uchun IsAdminOrOwnerInvoice ishlatiladi:
    admin barchasini ko'radi/o'zgartiradi, bemor esa faqat o'ziga tegishli
    hisob-fakturalarni ko'ra oladi.
    """
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers

    def get_queryset(self):
        """So'rov yuborgan foydalanuvchiga mos hisob-fakturalar ro'yxatini qaytaradi.

        Qaytaradi:
            QuerySet: admin uchun barcha Invoice'lar, aks holda faqat
            so'rov yuborgan bemorga tegishli Invoice'lar.
        """
        queryset = Invoice.objects.all()
        if self.request.user.role != 'admin':
            queryset = queryset.filter(patient__user=self.request.user)
        return queryset

    def get_permissions(self):
        """Amalga (action) qarab kerakli ruxsat sinflarini tanlaydi.

        Qaytaradi:
            list: 'create' amali uchun [IsAdmin()], aks holda
            [IsAdminOrOwnerInvoice()].
        """
        if self.action == 'create':
            return [IsAdmin()]
        return [IsAdminOrOwnerInvoice()]


class DoctorPayoutViewSet(viewsets.ModelViewSet):
    """Shifokor to'lovlari (DoctorPayout) uchun CRUD amallarini taqdim etuvchi ViewSet.

    Faqat admin yangi to'lov yarata oladi ('create' amali uchun IsAdmin
    talab qilinadi). Boshqa amallar uchun IsAdminOrOwnerPayout ishlatiladi:
    admin barchasini ko'radi/o'zgartiradi, shifokor esa faqat o'ziga
    tegishli to'lovlarni ko'ra oladi.
    """
    queryset = DoctorPayout.objects.all()
    serializer_class = DoctorPayoutSerializers

    def get_queryset(self):
        """So'rov yuborgan foydalanuvchiga mos to'lovlar ro'yxatini qaytaradi.

        Qaytaradi:
            QuerySet: admin uchun barcha DoctorPayout'lar, aks holda faqat
            so'rov yuborgan shifokorga tegishli DoctorPayout'lar.
        """
        queryset = DoctorPayout.objects.all()
        if self.request.user.role != 'admin':
            queryset = queryset.filter(doctor__user=self.request.user)
        return queryset

    def get_permissions(self):
        """Amalga (action) qarab kerakli ruxsat sinflarini tanlaydi.

        Qaytaradi:
            list: 'create' amali uchun [IsAdmin()], aks holda
            [IsAdminOrOwnerPayout()].
        """
        if self.action == 'create':
            return [IsAdmin()]
        return [IsAdminOrOwnerPayout()]

