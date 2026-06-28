from rest_framework import viewsets

from .models import Invoice, InsuranceClaim, DoctorPayout
from .serializers import InvoiceSerializers, InsuranceClaimSerializers, DoctorPayoutSerializers
from users.permissions import IsAdmin

class InvoiceViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers

class InsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InsuranceClaim.objects.all()
    serializer_class = InsuranceClaimSerializers

class DoctorPayoutViewSet(viewsets.ModelViewSet):
    queryset = DoctorPayout.objects.all()
    serializer_class = DoctorPayoutSerializers

