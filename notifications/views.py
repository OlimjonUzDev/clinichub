from rest_framework import viewsets

from .models import NotificationTemplate, NotficationLog
from .serializers import NotificationTemplateSerializers, NotificationLogSerializers
from users.permissions import IsAdmin

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializers

class NotificationLogViewSet(viewsets.ModelViewSet):
    queryset = NotficationLog.objects.all()
    serializer_class = NotificationLogSerializers
    
