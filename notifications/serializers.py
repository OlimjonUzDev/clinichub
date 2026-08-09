from rest_framework import serializers

from .models import NotificationTemplate, NotificationLog

class NotificationTemplateSerializers(serializers.ModelSerializer):
    """`NotificationTemplate` modelining barcha maydonlarini serializatsiya qiladi."""

    class Meta:
        model = NotificationTemplate
        fields = '__all__'

class NotificationLogSerializers(serializers.ModelSerializer):
    """`NotificationLog` modelining barcha maydonlarini serializatsiya qiladi."""

    class Meta:
        model = NotificationLog
        fields = '__all__'