from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Speciality, RankPrice, RankType
from clinics.models import Clinic

User = get_user_model()

class CatalogViewSetTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin1', password='adminpass1', role='admin')
        self.patient_user = User.objects.create_user(username='shahnoza', password='pass123', role='patient')

        self.speciality = Speciality.objects.create(name_uz='Terapevt', name_ru='Терапевт')
        self.rank_type = RankType.objects.create(name_uz='Oliy', name_ru='Высшая')

    def test_anonymous_can_list_specialities(self):
        url = reverse('speciality-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_specilaty(self):
        url = reverse('speciality-list')
        self.client.force_authenticate(user=None)
        response = self.client.post(url, {'name_uz': 'Kardiolog', 'name_ru': 'Кардиолог'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_admin_create_specilaty(self):
        url = reverse('speciality-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_specilatiy(self):
        url = reverse('speciality-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'name_uz': 'Terapeft', 'name_ru': 'Терапефт'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
