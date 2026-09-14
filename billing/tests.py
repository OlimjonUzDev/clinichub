from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
import datetime
from unittest.mock import patch

from .models import Invoice
from clinics.models import MedicalCenter, ClinicType, Clinic
from patients.models import Patient
from catalog.models import Speciality, RankType
from doctors.models import Doctor
from appointments.models import Appointment

User = get_user_model()

class BillingViewSetTestCase(APITestCase):

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

        self.appointment = Appointment.objects.create(
            patient=self.patient, doctor=self.doctor, clinic=self.clinic,
            start_time=timezone.make_aware(datetime.datetime(2026, 7, 18, 9, 30)),
            end_time=timezone.make_aware(datetime.datetime(2026, 7, 18, 9, 50)),
        )

        self.invoice = Invoice.objects.create(
            appointment=self.appointment, patient=self.patient,
            invoice_number='INV-001', amount=100000,
        )
        

    def test_admin_can_list_invoices(self):
        admin_user = User.objects.create_user(username='admin1', password='adminpass1', role='admin')
        url = reverse('invoice-list')
        self.client.force_authenticate(admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_can_list_own_invoice_only(self):
        other_user = User.objects.create_user(username='Baxti', password='qwerty55', role='patient')
        other_patient = Patient.objects.create(user=other_user, name_uz='Baxti', name_ru='Бахти', birth_date='2000-05-05')
        other_appointmen = Appointment.objects.create(patient=other_patient, doctor=self.doctor, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 7, 19, 9, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 7, 19, 9, 50)),)
        Invoice.objects.create(appointment=other_appointmen, patient=other_patient, invoice_number='INV-002', amount=50000)
        url = reverse('invoice-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invoice_ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.invoice.pk, invoice_ids)
        self.assertEqual(len(invoice_ids), 1)

    def test_owner_patient_can_retrieve_invoice(self):
        url = reverse('invoice-detail', args=[self.invoice.pk])
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_patient_cannot_retrieve_invoice(self):
        other_user = User.objects.create_user(username='Ali', password='qwerty11', role='patient')
        url = reverse('invoice-detail', args=[self.invoice.pk])
        self.client.force_authenticate(other_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patient_cannot_update_invoice(self):
        url = reverse('invoice-detail', args=[self.invoice.pk])
        self.client.force_authenticate(self.patient_user)
        response = self.client.patch(url, {'status': 'paid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_invoice(self):
        admin = User.objects.create_user(username='admin3', password='adminpass1', role='admin')
        url = reverse('invoice-detail', args=[self.invoice.pk])
        self.client.force_authenticate(admin)
        response = self.client.patch(url, {'status': 'paid'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, 'paid')




