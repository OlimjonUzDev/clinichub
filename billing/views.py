from rest_framework import viewsets

from .models import Invoice
from .serializers import InvoiceSerializers

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializers

