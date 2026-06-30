from rest_framework import viewsets

from .models import NotificationTemplate, NotificationLog
from .serializers import NotificationTemplateSerializers, NotificationLogSerializers
from users.permissions import IsAdmin

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializers

class NotificationLogViewSet(viewsets.ModelViewSet):
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializers
    
