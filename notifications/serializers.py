from rest_framework import serializers

from .models import NotificationTemplate

class NotificationTemplateSerializers(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = '__all__'