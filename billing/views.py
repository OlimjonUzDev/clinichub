from rest_framework import viewsets

from .models import Invoice, DoctorPayout
from .serializers import InvoiceSerializers, DoctorPayoutSerializers
from users.permissions import IsAdmin

class InvoiceViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers

class DoctorPayoutViewSet(viewsets.ModelViewSet):
    queryset = DoctorPayout.objects.all()
    serializer_class = DoctorPayoutSerializers

