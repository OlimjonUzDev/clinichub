from rest_framework import serializers

from .models import NotificationTemplate, NotficationLog

class NotificationTemplateSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'

class NotificationLogSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotficationLog
        fields = '__all__'