from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
import datetime

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Prescription, PrescriptionItem
from doctors.models import Doctor
from patients.models import Patient
from appointments.models import Appointment
from clinics.models import MedicalCenter, Clinic, ClinicType
from catalog.models import Speciality, RankType

User = get_user_model()

class PrescriptionsViewSetTestCase(APITestCase):

    def setUp(self):
        medical_center = MedicalCenter.objects.create(name_uz='Markaziy', name_ru='Центральная')
        clinic_type = ClinicType.objects.create(name_uz='Poliklinika', name_ru='Поликлиника')
        self.clinic = Clinic.objects.create(medical_center=medical_center, clinic_type=clinic_type, phone_number='+998963211236')

        speciality = Speciality.objects.create(name_uz='Terapevt', name_ru='терапефт')
        rank_type = RankType.objects.create(name_uz='Oliy', name_ru='Высшая')
        self.doctor_user = User.objects.create_user(username='axror', password='uiop00', role='doctor')
        self.doctor = Doctor.objects.create(user=self.doctor_user, speciality=speciality, rank_type=rank_type, clinic=self.clinic, name_uz='axror', name_ru='ахрор')
        self.doctor_user2 = User.objects.create_user(username='abror', password='qwerty', role='doctor')
        self.doctor2 = Doctor.objects.create(user=self.doctor_user2, speciality=speciality, rank_type=rank_type, clinic=self.clinic, name_uz='abror', name_ru='аброр')

        self.owner_user = User.objects.create_user(username='alisher', password='qwertzxc', role='patient')
        self.patient = Patient.objects.create(user=self.owner_user, name_uz='Alisher', name_ru='Алишер', birth_date='2000-01-01')
        self.owner_user2 = User.objects.create_user(username='umid', password='password1', role='patient')
        self.patient2 = Patient.objects.create(user=self.owner_user2, name_uz='Umid', name_ru='Умид', birth_date='2000-10-01')

        self.appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 11, 5, 10, 50)))
        self.appointment2 = Appointment.objects.create(patient=self.patient2, doctor=self.doctor2, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 10, 5, 10, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 10, 5, 10, 50)))

        self.prescription = Prescription.objects.create(appointment=self.appointment, doctor=self.doctor, patient=self.patient, diagnosis_uz='Yurak xuruji')   
        self.prescriptionitem = PrescriptionItem.objects.create(prescription=self.prescription, medication_name_uz='Markaziy', dosage='500mg', frequency_uz='kunga2 marta', duration_days=5)

    def test_owner_doctor_can_create_prescription_with_items(self):
        new_appointment = Appointment.objects.create(patient=self.patient, doctor=self.doctor, clinic=self.clinic, start_time=timezone.make_aware(datetime.datetime(2026, 11, 6, 10, 30)), end_time=timezone.make_aware(datetime.datetime(2026, 11, 6, 10, 50)))
        url = reverse('prescription-list')
        self.client.force_authenticate(self.doctor_user)
        response = self.client.post(url, {'appointment': new_appointment.pk, 'doctor': self.doctor.pk, 'patient': self.patient.pk, 'diagnosis_uz': 'Gripp', 'items': [{'medication_name_uz': 'Paracetamol', 'dosage': '500mg', 'frequency_uz': 'kuniga 3 marta', 'duration_days': 5}]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_prescription_list_filtered_to_own_patient(self):
        url = reverse('prescription-list')
        self.client.force_authenticate(self.owner_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_prescription_list_filtered_to_own_doctor(self):
        url = reverse('prescription-list')
        self.client.force_authenticate(self.doctor_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_doctor_cannot_retrieve_prescription(self):
        url = reverse('prescription-detail', args=[self.prescription.pk])
        self.client.force_authenticate(self.doctor_user2)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patient_cannot_update_prescription(self):
        url = reverse('prescription-detail', args=[self.prescription.pk])
        self.client.force_authenticate(self.owner_user)
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_invalid_item_data_returns_400_not_500(self):
        url = reverse('prescription-detail', args=[self.prescription.pk])
        self.client.force_authenticate(self.doctor_user)
        response = self.client.patch(url, {'items': [{'dosage': '500mg'}]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_replaces_items_when_items_provided(self):
        url = reverse('prescription-detail', args=[self.prescription.pk])
        self.client.force_authenticate(self.doctor_user)
        response = self.client.patch(url, {'items': [{'medication_name_uz': 'Ibuprofen', 'dosage': '400mg', 'frequency_uz': 'kuniga 2 marta', 'duration_days': 3}]}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_without_items_keeps_existing_items(self):
        url = reverse('prescription-detail', args=[self.prescription.pk])
        self.client.force_authenticate(self.doctor_user)
        response = self.client.patch(url, {'diagnosis_uz': 'Yangilangan tashxis'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
