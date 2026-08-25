from rest_framework import serializers

from .models import Conversation, Message

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'conversation']