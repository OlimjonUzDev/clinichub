from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch

from .models import Payment, PaymentTransaction
from patients.models import Patient
from billing.models import Invoice
from clinics.models import MedicalCenter, Clinic, ClinicType
from catalog.models import Speciality, RankType
from doctors.models import Doctor
from appointments.models import Appointment

User = get_user_model()

class PaymentsViewSetTestCase(APITestCase):

    def setUp(self):
        patcher = patch('appointments.signals.send_sms')
        self.mock_send_sms = patcher.start()
        self.addCleanup(patcher.stop)

        medical_center = MedicalCenter.objects.create(name_uz='Markaziy', name_ru='Центральная')
        clinic_type = ClinicType.objects.create(name_uz='Poliklinika', name_ru='Поликлиника')
        self.clinic = Clinic.objects.create(medical_center=medical_center, clinic_type=clinic_type, phone_number='+998963211236')

        self.owner_user = User.objects.create_user(username='alisher', password='qwertzxc', role='patient')
        self.patient = Patient.objects.create(user=self.owner_user, name_uz='Alisher', name_ru='Алишер', birth_date='2000-01-01')
        self.other_patient_user = User.objects.create_user(username='xamid', password='xamid222', role='patient')
        self.admin_user = User.objects.create_user(username='akmla', password='qwert00', role='admin')

        speciality = Speciality.objects.create(name_uz='Terapevt', name_ru='терапефт')
        rank_type = RankType.objects.create(name_uz='Oliy', name_ru='Высшая')
        self.doctor_user = User.objects.create_user(username='axror', password='uiop00', role='doctor')
        self.doctor = Doctor.objects.create(user=self.doctor_user, speciality=speciality, rank_type=rank_type, clinic=self.clinic, name_uz='abror', name_ru='аброр')

        self.appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 50)))
        self.invoice = Invoice.objects.create(appointment=self.appointment, patient=self.patient, invoice_number='INV-P001', amount=100000)

        self.payment = Payment.objects.create(invoice=self.invoice, patient=self.patient, provider='stripe', amount=100000)

    def test_patient_can_list_own_payments_only(self):
        other_patient = Patient.objects.create(user=self.other_patient_user, name_uz='Baxti', name_ru='Бахти', birth_date='2000-05-05')
        other_appointmen = Appointment.objects.create(patient=other_patient, doctor=self.doctor, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 7, 19, 9, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 7, 19, 9, 50)),)
        other_invoice = Invoice.objects.create(appointment=other_appointmen, patient=other_patient, invoice_number='INV-003', amount=70000)
        Payment.objects.create(invoice=other_invoice, patient=other_patient, provider='stripe', amount=70000)
        url = reverse('payment-list')
        self.client.force_authenticate(self.owner_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment_ids = [item['id'] for item in response.data['results']]
        self.assertIn(self.payment.pk, payment_ids)
        self.assertEqual(len(payment_ids), 1)

    def test_admin_can_list_payments(self):
        url = reverse('payment-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_payment_amount_mismatch_rejected(self):
        url = reverse('payment-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'invoice': self.invoice.pk, 'patient': self.patient.pk, 'provider': 'stripe', 'amount': 50000}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_for_already_paid_invoice_rejected(self):
        paid_appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 50)))
        paid_invoice = Invoice.objects.create(appointment=paid_appointment, patient=self.patient, invoice_number='INV-P002', amount=200000, status='paid')
        url = reverse('payment-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'invoice': paid_invoice.pk, 'patient': self.patient.pk, 'provider': 'stripe', 'amount': 200000}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_payment_valid_succeeds(self):
        url = reverse('payment-list')
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(url, {'invoice': self.invoice.pk, 'patient': self.patient.pk, 'provider': 'stripe', 'amount': 100000}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch('payments.views.stripe.PaymentIntent.create')
    def test_create_stripe_intent_for_own_payment(self, mock_create):
        mock_create.return_value.id = 'pi_test123'
        mock_create.return_value.client_secret = 'secret_test123'

        url = reverse('stripe-create-intent')
        self.client.force_authenticate(self.owner_user)
        response = self.client.post(url, {'payment_id': self.payment.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['client_secret'], 'secret_test123')

    def test_create_stripe_intent_for_other_patient_payment_returns_404(self):
        url = reverse('stripe-create-intent')
        self.client.force_authenticate(self.other_patient_user)
        response = self.client.post(url, {'payment_id': self.payment.pk}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_stripe_webhook_invalid_signature_rejected(self):
        url = reverse('stripe-webhook')
        self.client.force_authenticate(user=None)
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



        

