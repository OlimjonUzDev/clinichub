from rest_framework import viewsets

from .models import Invoice
from .serializers import InvoiceSerializers
from users.permissions import IsAdmin

class InvoiceViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers

