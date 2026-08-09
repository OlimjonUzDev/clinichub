from rest_framework import viewsets

from .models import NotificationTemplate, NotificationLog
from .serializers import NotificationTemplateSerializers, NotificationLogSerializers
from users.permissions import IsAdmin

class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """Xabarnoma shablonlari (`NotificationTemplate`) uchun CRUD API.

    Faqat admin huquqiga ega foydalanuvchilar (`IsAdmin`) shablonlarni
    ko'rishi, yaratishi, tahrirlashi va o'chirishi mumkin.
    """

    permission_classes = [IsAdmin]
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializers

class NotificationLogViewSet(viewsets.ModelViewSet):
    """Yuborilgan xabarnomalar tarixi (`NotificationLog`) uchun CRUD API.

    Faqat admin huquqiga ega foydalanuvchilar (`IsAdmin`) xabarnoma
    yozuvlarini ko'rishi, yaratishi, tahrirlashi va o'chirishi mumkin.
    """

    permission_classes = [IsAdmin]
    queryset = NotificationLog.objects.all()
    serializer_class = NotificationLogSerializers
    
