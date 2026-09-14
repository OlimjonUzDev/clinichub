import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from appointments.models import Appointment
from catalog.models import RankType, Speciality
from clinics.models import Clinic, ClinicType, MedicalCenter
from doctors.models import Doctor
from patients.models import Patient
from billing.models import Invoice

from .models import Conversation, Message

User = get_user_model()


class ChatMessageTestCase(APITestCase):

    def setUp(self):
        medical_center = MedicalCenter.objects.create(name_uz='Markaziy', name_ru='Центральная')
        clinic_type = ClinicType.objects.create(name_uz='Poliklinika', name_ru='Поликлиника')
        clinic = Clinic.objects.create(medical_center=medical_center, clinic_type=clinic_type, phone_number='+998963211236')

        speciality = Speciality.objects.create(name_uz='Terapevt', name_ru='терапефт')
        rank_type = RankType.objects.create(name_uz='Oliy', name_ru='Высшая')

        self.doctor_user = User.objects.create_user(username='doctor1', password='pass1234', role='doctor')
        self.doctor = Doctor.objects.create(user=self.doctor_user, speciality=speciality, rank_type=rank_type, clinic=clinic, name_uz='Doktor', name_ru='Доктор')

        self.patient_user = User.objects.create_user(username='patient1', password='pass1234', role='patient')
        self.patient = Patient.objects.create(user=self.patient_user, name_uz='Bemor', name_ru='Пациент', birth_date='2000-01-01')

        self.stranger_user = User.objects.create_user(username='stranger', password='pass1234', role='patient')

        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, clinic=clinic,
            start_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 30)),
            end_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 50)),
        )
        self.other_appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, clinic=clinic,
            start_time=timezone.make_aware(datetime.datetime(2026, 11, 6, 10, 30)),
            end_time=timezone.make_aware(datetime.datetime(2026, 11, 6, 10, 50)),
        )
        Invoice.objects.create(
            appointment=self.appointment, patient=self.patient,
            invoice_number='INV-CHAT-001', amount=100000, status='paid',
        )
        Invoice.objects.create(
            appointment=self.other_appointment, patient=self.patient,
            invoice_number='INV-CHAT-002', amount=100000, status='paid',
        )
        self.url = reverse('chat-message-list')

    def test_unauthenticated_cannot_list(self):
        response = self.client.get(self.url, {'appointment_id': self.appointment.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_participant_can_list(self):
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(self.url, {'appointment_id': self.appointment.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_participant_can_list(self):
        self.client.force_authenticate(self.doctor_user)
        response = self.client.get(self.url, {'appointment_id': self.appointment.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stranger_cannot_list(self):
        self.client.force_authenticate(self.stranger_user)
        response = self.client.get(self.url, {'appointment_id': self.appointment.pk})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_participant_can_create_message_and_conversation_is_created(self):
        self.client.force_authenticate(self.patient_user)
        response = self.client.post(self.url, {'appointment_id': self.appointment.pk, 'text': 'Salom, doktor!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Conversation.objects.filter(appointment=self.appointment).exists())
        self.assertEqual(response.data['sender'], self.patient_user.pk)

    def test_stranger_cannot_create_message(self):
        self.client.force_authenticate(self.stranger_user)
        response = self.client.post(self.url, {'appointment_id': self.appointment.pk, 'text': 'Salom'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Message.objects.filter(text='Salom').exists())

    def test_history_filtered_to_requested_appointment_only(self):
        conversation = Conversation.objects.create(appointment=self.appointment)
        other_conversation = Conversation.objects.create(appointment=self.other_appointment)
        Message.objects.create(conversation=conversation, sender=self.patient_user, text='Bu appointment 1')
        Message.objects.create(conversation=other_conversation, sender=self.patient_user, text='Bu appointment 2')

        self.client.force_authenticate(self.patient_user)
        response = self.client.get(self.url, {'appointment_id': self.appointment.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        texts = [m['text'] for m in response.data['results']]
        self.assertIn('Bu appointment 1', texts)
        self.assertNotIn('Bu appointment 2', texts)