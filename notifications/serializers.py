from rest_framework import serializers

from .models import NotificationTemplate, NotificationLog

class NotificationTemplateSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'

class NotificationLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotificationLog
        fields = '__all__'