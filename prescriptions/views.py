from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Prescription, PrescriptionItem
from .serializers import PrescriptionSerializer, PrescriptionItemSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer

    def get_queryset(self):
        queryset = Prescription.objects.all()

        # GET /api/v1/prescriptions/prescription/?patient_id=8
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        # GET /api/v1/prescriptions/prescription/?appointment_id=5
        appointment_id = self.request.query_params.get('appointment_id')
        if appointment_id:
            queryset = queryset.filter(appointment_id=appointment_id)

        return queryset


class PrescriptionItemViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = PrescriptionItem.objects.all()
    serializer_class = PrescriptionItemSerializer
