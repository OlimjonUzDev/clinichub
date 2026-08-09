from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializers
from .permissions import IsAdminOrDoctor, IsAdminOrOwnerPatient
from users.permissions import IsAdmin

class CustomPagination(PageNumberPagination):
    page_size = 6

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializers
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name_uz', 'name_ru']

    def get_queryset(self):
        user = self.request.user
        if user.role in ('admin', 'doctor'):
            return Patient.objects.all()
        return Patient.objects.filter(user=user)

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdminOrDoctor()]
        if self.action in ['create', 'destroy']:
            return [IsAdmin()]
        return [IsAdminOrOwnerPatient()]

    @action(detail=False, methods=['get', 'post', 'patch'])
    def me(self, request):
        patient = Patient.objects.filter(user=request.user).first()

        if request.method == 'GET':
            if not patient:
                return Response({'detail': 'Patient profili topilmadi'}, status=400)
            return Response(self.get_serializer(patient).data)

        if request.method == 'POST':
            if patient:
                return Response({'detail': 'Patient profili allaqachon mavjud'}, status=400)
            serializer = self.get_serializer(data=request.data)
            serializer.fields.pop('user', None)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        if not patient:
            return Response({'detail': 'Patient profili topilmadi'}, status=400)
        serializer = self.get_serializer(patient, data=request.data, partial=True)
        serializer.fields.pop('user', None)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

