from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from .models import Appointment, Rating
from .serializers import AppointmentSerializers, RatingSerializers
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsPatient
from .permissions import IsAdminOrOwnerAppointments, IsAdminOrOwnerRating

class CustomPagination(PageNumberPagination):
    page_size = 6

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['patient__name_uz', 'patient__name_ru']

    def create(self, request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        if request.user.role == 'patient':
            serializers.fields.pop('patient', None)
            patient = getattr(request.user, 'patient', None)
            if not patient:
                return Response({'detail': 'Avval bemor profilingizni yarating'}, status=400)

        serializers.is_valid(raise_exception=True)

        if request.user.role == 'patient':
            serializers.save(patient=patient)
        else:
            serializers.save()

        headers = self.get_success_headers(serializers.data)
        return Response(serializers.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Appointment.objects.all()
        return Appointment.objects.filter(Q(patient__user=user) | Q(doctor__user=user))

    def get_permissions(self):
        if self.action in ['list', 'create']:
            return [IsAuthenticated()]
        return [IsAdminOrOwnerAppointments()]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.validated_data['appointment']
        serializer.save(patient=appointment.patient, doctor=appointment.doctor)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Rating.objects.all()
        return Rating.objects.filter(Q(patient__user=user) | Q(doctor__user=user))

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsPatient()]
        return [IsAdminOrOwnerRating()]

