from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
import datetime
from unittest.mock import patch

from .models import Appointment, Rating
from .views import AppointmentViewSet
from clinics.models import MedicalCenter, ClinicType, Clinic
from patients.models import Patient
from catalog.models import Speciality, RankType
from doctors.models import Doctor, DoctorSchedule

User = get_user_model()

class AppointmentViewSetTestCase(APITestCase):

    def setUp(self):
       patcher = patch('appointments.signals.send_sms')
       self.mock_send_sms = patcher.start()
       self.addCleanup(patcher.stop)

       medical_center = MedicalCenter.objects.create(name_uz='Markaziy', name_ru='Центральный')
       clinic_type = ClinicType.objects.create(name_uz='Poliklinika', name_ru='Поликлиника')
       self.clinic = Clinic.objects.create(medical_center=medical_center, clinic_type=clinic_type, phone_number='+998901231232')

       self.patient_user = User.objects.create_user(username='shahnoza', password='pass123', role='patient')
       self.patient = Patient.objects.create(user=self.patient_user, name_uz='Shahnoza', name_ru='Шахноза', birth_date='2000-05-05')

       speciality = Speciality.objects.create(name_uz='Terapevt', name_ru='терапефт')
       rank_type = RankType.objects.create(name_uz='Oliy', name_ru='Высшая')
       self.doctor_user = User.objects.create_user(username='Suxrob', password='qwerty123', role='doctor')
       self.doctor = Doctor.objects.create(user=self.doctor_user, speciality=speciality, rank_type=rank_type, clinic=self.clinic, name_uz='Suxrob', name_ru='Сухроб')
       self.appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 7, 18, 9, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 7, 18, 9, 50)))

       self.doctor_schedule = DoctorSchedule.objects.create(doctor=self.doctor, weekday=5, start_time='08:00', end_time='18:00')

    def test_appointment_list(self):
        url = reverse('appointment-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_dendied_for_anonymous_create(self):
        self.client.force_authenticate(user=None)
        url = reverse('appointment-list')
        data = {'patient': self.patient.pk, 'doctor': self.doctor.pk, 'clinic': self.clinic.pk,
                'start_time': timezone.make_aware(datetime.datetime(2026, 7, 19, 10, 0)),
                'end_time': timezone.make_aware(datetime.datetime(2026, 7, 19, 10, 20)),}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_cannot_retrieve(self):
        url = reverse('appointment-detail', args=[self.appointment.pk])
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_owner_can_retrieve(self):
        url = reverse('appointment-detail', args=[self.appointment.pk])
        self.client.force_authenticate(self.patient.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_patient_cannot_retrieve(self):
        self.patient_user2 = User.objects.create_user(username='abdumalik', password='zxcv345', role='patient')
        self.patient2 = Patient.objects.create(user=self.patient_user2, name_uz='Abdumalik', name_ru='Абдумалик', birth_date='2001-01-01')
        url = reverse('appointment-detail', args=[self.appointment.pk])
        self.client.force_authenticate(self.patient_user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_doctor_can_update(self):
        url = reverse('appointment-detail', args=[self.appointment.pk])
        self.client.force_authenticate(self.doctor_user)
        response = self.client.patch(url, {'notes': 'Yangilangan izoh'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_update_any_appointment(self):
        admin_user = User.objects.create_user(username='admin3', password='iyuth11', role='admin')
        url = reverse('appointment-detail', args=[self.appointment.pk])
        self.client.force_authenticate(admin_user)
        response = self.client.patch(url, {'status': 'confirmed'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_end_time_before_start_time_rejected(self):
        url = reverse('appointment-list')
        self.client.force_authenticate(self.patient_user)
        data = {'patient': self.patient.pk, 'doctor': self.doctor.pk, 'clinic': self.clinic.pk,
                'start_time': timezone.make_aware(datetime.datetime(2026, 7, 25, 10, 20)),
                'end_time': timezone.make_aware(datetime.datetime(2026, 7, 25, 10, 00)),}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_double_booking_rejected(self):
        url = reverse('appointment-list')
        self.client.force_authenticate(self.patient_user)
        data = {'patient': self.patient.pk, 'doctor': self.doctor.pk, 'clinic': self.clinic.pk,
                'start_time': timezone.make_aware(datetime.datetime(2026, 7, 18, 9, 40)),
                'end_time': timezone.make_aware(datetime.datetime(2026, 7, 18, 10, 00)),}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Doktor bu vaqt band", str(response.data))

    def test_no_schedule_day_rejected(self):
        url = reverse('appointment-list')
        self.client.force_authenticate(self.patient_user)
        data = {'patient': self.patient.pk, 'doctor': self.doctor.pk, 'clinic': self.clinic.pk,
                'start_time': timezone.make_aware(datetime.datetime(2026, 7, 19, 10, 20)),
                'end_time': timezone.make_aware(datetime.datetime(2026, 7, 19, 10, 40)),}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Doktor bu kun ishlamaydi', str(response.data))

    def test_outside_schedule_hours_rejected(self):
        url = reverse('appointment-list')
        self.client.force_authenticate(self.patient_user)
        data = {'patient': self.patient.pk, 'doctor': self.doctor.pk, 'clinic': self.clinic.pk,
                'start_time': timezone.make_aware(datetime.datetime(2026, 7, 25, 19, 20)),
                'end_time': timezone.make_aware(datetime.datetime(2026, 7, 25, 19, 40)),}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Vaqt doktorning ish jadvalidan tashqarida", str(response.data))

    def test_valid_appointment_created_successfully(self):
        url = reverse('appointment-list')
        self.client.force_authenticate(self.patient_user)
        data = {'patient': self.patient.pk, 'doctor': self.doctor.pk, 'clinic': self.clinic.pk,
                'start_time': timezone.make_aware(datetime.datetime(2026, 7, 25, 15, 20)),
                'end_time': timezone.make_aware(datetime.datetime(2026, 7, 25, 15, 40)),}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)