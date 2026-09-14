from rest_framework import viewsets

from .models import Message, Conversation
from .serializers import MessageSerializers
from .permissions import IsAppointmentParticipant


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializers
    permission_classes = [IsAppointmentParticipant]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        appointment_id = self.request.query_params.get('appointment_id')
        return Message.objects.filter(conversation__appointment_id=appointment_id)

    def perform_create(self, serializer):
        appointment_id = self.request.data.get('appointment_id')
        conversation, _ = Conversation.objects.get_or_create(appointment_id=appointment_id)
        serializer.save(sender=self.request.user, conversation=conversation)