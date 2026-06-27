from rest_framework import viewsets

from .models import NotificationTemplate
from .serializers import NotificationTemplateSerializers
from users.permissions import IsAdmin

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializers
    
