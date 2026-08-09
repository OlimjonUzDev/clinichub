from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from .models import NotificationLog, NotificationTemplate

User = get_user_model()

class NotificationsViewSetTestCase(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin5', password='yuiop', role='admin')
        self.patient_user = User.objects.create_user(username='patient4', password='zxcvb', role='patient')

        self.template = NotificationTemplate.objects.create(name='Appointment Reminder', body_uz='Sizning qabulingiz ertaga soat 10:00 da', body_ru='ваш прием завтра в 10:00', type='sms')
        self.log = NotificationLog.objects.create(user=self.patient_user, template=self.template, message='Sizning qabulingiz ertaga soat 10:00 da', type='sms')

    def test_anonymous_cannot_access_template(self):
        url = reverse('notificationtemplate-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_cannot_create_template(self):
        url = reverse('notificationtemplate-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_template(self):
        url = reverse('notificationtemplate-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'name': 'Payment Confirmation','body_uz': 'Tolovingiz muvaffaqiyatli amalga oshirildi','body_ru': 'Ваш платеж успешно выполнен','type': 'email'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_can_delete_template(self):
        url = reverse('notificationtemplate-detail', args=[self.template.id])
        self.client.force_authenticate(self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_anonymous_cannot_access_log(self):
        url = reverse('notificationlog-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_cannot_retrieve_log(self):
        url = reverse('notificationlog-detail', args=[self.log.pk])
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_list_log(self):
        url = reverse('notificationlog-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_log(self):
        url = reverse('notificationlog-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'user': self.patient_user.id, 'template': self.template.id, 'message': 'Sizning navbatingiz bekor qilindi', 'type': 'push'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)