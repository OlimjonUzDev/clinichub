from rest_framework import serializers

from .models import MessageTemplate

class MessageTemplateSerializers(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'