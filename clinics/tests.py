from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

from .models import MedicalCenter, Clinic, ClinicType

User = get_user_model()

class ClinicsViewSetTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin6', password='apatey', role='admin')
        self.patient_user = User.objects.create_user(username='password', password='kjhbk', role='patient')

        self.medical_center = MedicalCenter.objects.create(name_uz='Markaziy kilinka', name_ru='Центральная клиника')
        self.clinic_type = ClinicType.objects.create(name_uz ='Poliklinika', name_ru='Поликлиника')
        self.clinic = Clinic.objects.create(medical_center=self.medical_center, clinic_type=self.clinic_type, phone_number='+998974563210')

    def test_anonymous_can_list_medicalcenters(self):
        url = reverse('medicalcenter-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_medicalcenter(self):
        url = reverse('medicalcenter-list')
        self.client.force_authenticate(user=None)
        response = self.client.post(url, {'name_uz': 'Markaziy kilinka', 'name_ru': 'Центральная поликлиника'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_cannot_create_medicalcenter(self):
        url = reverse('medicalcenter-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_medicalcenter(self):
        url = reverse('medicalcenter-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'name_uz': 'Terapeft', 'name_ru': 'Терапефт'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_anonymous_can_list_clinics(self):
        url = reverse('clinic-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_clinics(self):
        url = reverse('clinic-list')
        self.client.force_authenticate(user=None)
        response = self.client.post(url, {'medical_center': self.medical_center.pk, 'clinic_type': self.clinic_type.pk, 'phone_number': '+998961235469'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_cannot_create_clinic(self):
        url = reverse('clinic-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_clinic(self):
        url = reverse('clinic-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'medical_center': self.medical_center.pk, 'clinic_type': self.clinic_type.pk, 'phone_number': '+998901236549'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) 



