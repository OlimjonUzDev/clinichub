from rest_framework import viewsets

from .models import MessageTemplate
from .serializers import MessageTemplateSerializers
from users.permissions import IsAdmin

class MessageTemplateViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializers
    
