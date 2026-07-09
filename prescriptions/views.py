from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Prescription, PrescriptionItem
from .serializers import PrescriptionSerializer, PrescriptionItemSerializer
from .permissions import IsAdminOrOwnerPrescription, IsAdminOrOwnerPrescriptionItem


class PrescriptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrOwnerPrescription]
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
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
    permission_classes = [IsAdminOrOwnerPrescriptionItem]
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer

    def get_queryset(self):
        queryset = PrescriptionItem.objects.all()
        user = self.request.user

        if user.role == 'patient':
            queryset = queryset.filter(prescription__patient__user=user)
        elif user.role == 'doctor':
            queryset = queryset.filter(prescription__doctor__user=user)
        return queryset
