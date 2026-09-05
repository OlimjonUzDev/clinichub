from rest_framework import viewsets

from .models import Invoice, DoctorPayout
from .serializers import InvoiceSerializers, DoctorPayoutSerializers
from users.permissions import IsAdmin
from .permissions import IsAdminOrOwnerInvoice, IsAdminOrOwnerPayout

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers

    def get_queryset(self):
        queryset = Invoice.objects.all()
        user = self.request.user
        if user.role == 'admin':
            return queryset
        if user.role == 'doctor':
            return queryset.filter(appointment__doctor__user=user)
        return queryset.filter(patient__user=user)

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin()]
        return [IsAdminOrOwnerInvoice()]
        

class DoctorPayoutViewSet(viewsets.ModelViewSet):
    queryset = DoctorPayout.objects.all()
    serializer_class = DoctorPayoutSerializers

    def get_queryset(self):
        queryset = DoctorPayout.objects.all()
        if self.request.user.role != 'admin':
            queryset = queryset.filter(doctor__user=self.request.user)
        return queryset

    def get_permissions(self):
        if self.action == 'create':
            return [IsAdmin()]
        return [IsAdminOrOwnerPayout()]

