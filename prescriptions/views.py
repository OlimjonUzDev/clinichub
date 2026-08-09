from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Prescription, PrescriptionItem
from .serializers import PrescriptionSerializer, PrescriptionItemSerializer
from .permissions import IsAdminOrOwnerPrescription, IsAdminOrOwnerPrescriptionItem


class PrescriptionViewSet(viewsets.ModelViewSet):
    """Retseptlar uchun CRUD endpointlarini taqdim etadi.

    Ruxsat IsAdminOrOwnerPrescription orqali boshqariladi: admin barcha
    retseptlarga, bemor va shifokor esa faqat o'ziga tegishli retseptlarga
    kira oladi. Ro'yxatni `patient_id` va `appointment_id` query parametrlari
    orqali qo'shimcha filtrlash mumkin.
    """

    permission_classes = [IsAdminOrOwnerPrescription]
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        """Joriy foydalanuvchining roli va query parametrlariga mos retseptlar ro'yxatini qaytaradi.

        Bemor uchun faqat o'ziga tegishli, shifokor uchun faqat o'zi yozgan
        retseptlar qaytariladi. Qo'shimcha ravishda `patient_id` va
        `appointment_id` query parametrlari orqali natija filtrlanadi.

        Qaytaradi:
            QuerySet: joriy foydalanuvchi va filtrlarga mos Prescription obyektlari.
        """
        queryset = Prescription.objects.all()
        user = self.request.user

        if user.role == 'patient':
            queryset = queryset.filter(patient__user=user)
        elif user.role == 'doctor':
            queryset = queryset.filter(doctor__user=user)

        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        appointment_id = self.request.query_params.get('appointment_id')
        if appointment_id:
            queryset = queryset.filter(appointment_id=appointment_id)
        return queryset


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    """Retsept bandlari (dori-darmonlar) uchun CRUD endpointlarini taqdim etadi.

    Ruxsat IsAdminOrOwnerPrescriptionItem orqali boshqariladi: admin barcha
    bandlarga, bemor va shifokor esa faqat o'zlariga tegishli retseptning
    bandlariga kira oladi.
    """

    permission_classes = [IsAdminOrOwnerPrescriptionItem]
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer

    def get_queryset(self):
        """Joriy foydalanuvchining roliga mos retsept bandlari ro'yxatini qaytaradi.

        Bemor uchun faqat o'ziga tegishli retseptlarning bandlari, shifokor
        uchun esa faqat o'zi yozgan retseptlarning bandlari qaytariladi.

        Qaytaradi:
            QuerySet: joriy foydalanuvchiga mos PrescriptionItem obyektlari.
        """
        queryset = PrescriptionItem.objects.all()
        user = self.request.user

        if user.role == 'patient':
            queryset = queryset.filter(prescription__patient__user=user)
        elif user.role == 'doctor':
            queryset = queryset.filter(prescription__doctor__user=user)
        return queryset
