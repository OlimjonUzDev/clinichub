from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Patient

User = get_user_model()

class PatientsViewSetTestCase(APITestCase):

    def setUp(self):
       self.owner_user = User.objects.create_user(username='alisher', password='qwertzxc', role='patient')
       self.patient = Patient.objects.create(user=self.owner_user, name_uz='Alisher', name_ru='Алишер', birth_date='2000-01-01')

       self.other_patient_user = User.objects.create_user(username='xamid', password='xamid222', role='patient')

       self.admin_user = User.objects.create_user(username='admin1', password='zxvbcn', role='admin')

       self.doctor_user = User.objects.create_user(username='doctor4', password='gfhjgk', role='doctor')

    def test_admin_or_doctor_can_list_patient(self):
        url = reverse('patient-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_cannot_list_patients(self):
        url = reverse('patient-list')
        self.client.force_authenticate(self.owner_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cannot_retrieve_patient(self):
        url = reverse('patient-detail', args=[self.patient.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_other_patient_cannot_retrieve_patient(self):
        url = reverse('patient-detail', args=[self.patient.pk])
        self.client.force_authenticate(self.other_patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_can_retrieve_own_patient(self):
        url = reverse('patient-detail', args=[self.patient.pk])
        self.client.force_authenticate(self.owner_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_ccan_update_own_patient(self):
        url = reverse('patient-detail', args=[self.patient.pk])
        self.client.force_authenticate(self.owner_user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_patient_cannot_update_patient(self):
        url = reverse('patient-detail', args=[self.patient.pk])
        self.client.force_authenticate(self.other_patient_user)
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_non_admin_cannot_create_patient(self):
        url = reverse('patient-list')
        self.client.force_authenticate(self.owner_user)
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_patient(self):
        new_user = User.objects.create_user(username='ali', password='zxcvbn', role='patient')
        url = reverse('patient-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'user': new_user.pk, 'name_uz': 'Aziza', 'name_ru': 'Азиза', 'birth_date': '2000-01-01',})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_doctor_cannot_retrieve_single_patient(self):
        url = reverse('patient-detail', args=[self.patient.pk])
        self.client.force_authenticate(self.doctor_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)