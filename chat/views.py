from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(detail=False, methods=['post'])
    def mark_read(self, request):
        appointment_id = request.data.get('appointment_id')
        Message.objects.filter(
            conversation__appointment_id=appointment_id
        ).exclude(sender=request.user).update(is_read=True)
        return Response({'detail': 'OK'})