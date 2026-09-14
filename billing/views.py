from rest_framework import viewsets

from .models import Invoice
from .serializers import InvoiceSerializers
from users.permissions import IsAdmin
from .permissions import IsAdminOrOwnerInvoice

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
        
