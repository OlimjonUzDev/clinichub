from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserViewSetTestCase(APITestCase):
    """Ro'yxatdan o'tish, foydalanuvchilar ro'yxati va dashboard endpointlarini tekshiradi."""

    def setUp(self):
        """Testlar uchun admin va patient rolidagi foydalanuvchilarni yaratadi."""

        self.admin_user = User.objects.create_user(username='ali', password='password33', role='admin')
        self.patient_user = User.objects.create_user(username='shara', password='qwdertbbn', role='patient')

    def test_register_creates_patient_role_regardless_of_payload(self):
        """Ro'yxatdan o'tishda so'rovda 'admin' roli yuborilsa ham, foydalanuvchiga 'patient' roli berilishini tekshiradi."""
        url = '/api/v1/register/'
        self.client.force_authenticate()
        response = self.client.post(url, {'username': 'newuser1', 'email': 'newuser1@test.com', 'password': 'Qwerty#Str0ng9', 'phone_number': '', 'role': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(username='newuser1').role, 'patient')

    def test_register_rejects_weak_password(self):
        """Zaif parol bilan ro'yxatdan o'tish 400 status bilan rad etilishini tekshiradi."""
        url = '/api/v1/register/'
        self.client.force_authenticate()
        response = self.client.post(url, {'username': 'newuser2', 'email': 'newuser2@test.com', 'password': '12345', 'phone_number': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_response_does_not_include_password(self):
        """Ro'yxatdan o'tish javobida parol maydoni qaytarilmasligini tekshiradi."""
        url = '/api/v1/register/'
        self.client.force_authenticate()
        response = self.client.post(url, {'username': 'newuser1', 'email': 'newuser1@test.com', 'password': 'Qwerty#Str0ng9', 'phone_number': '', 'role': 'admin'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn('password', response.data)

    def test_non_admin_cannot_list_users(self):
        """Admin bo'lmagan foydalanuvchi foydalanuvchilar ro'yxatiga kira olmasligini (403) tekshiradi."""
        url = '/api/v1/users/'
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_users(self):
        """Admin foydalanuvchi foydalanuvchilar ro'yxatiga muvaffaqiyatli kira olishini (200) tekshiradi."""
        url = '/api/v1/users/'
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_cannot_access_dashboard(self):
        """Admin bo'lmagan foydalanuvchi dashboard endpointiga kira olmasligini (403) tekshiradi."""
        url = '/api/v1/dashboard/'
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_access_dashboard(self):
        """Admin foydalanuvchi dashboard endpointiga muvaffaqiyatli kira olishini (200) tekshiradi."""
        url = '/api/v1/dashboard/'
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
