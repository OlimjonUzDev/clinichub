from rest_framework import viewsets

from .models import Invoice, DoctorPayout
from .serializers import InvoiceSerializers, DoctorPayoutSerializers
from users.permissions import IsAdmin
from .permissions import IsAdminOrOwnerInvoice, IsAdminOrOwnerPayout

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdmin()]
        return [IsAdminOrOwnerInvoice()]
        

class DoctorPayoutViewSet(viewsets.ModelViewSet):
    queryset = DoctorPayout.objects.all()
    serializer_class = DoctorPayoutSerializers

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAdmin()]
        return [IsAdminOrOwnerPayout()]

