from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Doctor, DoctorSchedule
from catalog.models import Speciality, RankType
from clinics.models import Clinic, MedicalCenter, ClinicType

User = get_user_model()

class DoctorsViewSetTestCase(APITestCase):
    """``DoctorViewSet`` va ``DoctorScheduleViewSet`` endpointlarining ruxsatlari va xatti-harakatini tekshiradi."""

    def setUp(self):
        """Testlar uchun admin, bemor va shifokor foydalanuvchilarini hamda tegishli klinika/shifokor ma'lumotlarini tayyorlaydi."""
        self.admin_user = User.objects.create_user(username='admin1', password='qwert00', role='admin')
        self.patient_user = User.objects.create_user(username='patient1', password='qwertyss', role='patient')
        self.doctor_user = User.objects.create_user(username='doctor1', password='asdfg', role='doctor')

        self.medical_center = MedicalCenter.objects.create(name_uz='', name_ru='')
        self.clinic_type = ClinicType.objects.create(name_uz='', name_ru='')
        self.clinic = Clinic.objects.create(medical_center=self.medical_center, clinic_type=self.clinic_type, phone_number='+998901234567')
        self.speciality = Speciality.objects.create(name_uz='Terapevt', name_ru='Терапевт')
        self.rank_type = RankType.objects.create(name_uz='Oliy', name_ru='Высшая')

        self.doctor = Doctor.objects.create(user=self.doctor_user, speciality=self.speciality, rank_type=self.rank_type, clinic=self.clinic, name_uz='Zafar', name_ru='Зафар')

    def test_anonymous_cannot_list_doctor(self):
        """Anonim foydalanuvchi ham shifokorlar ro'yxatini ko'ra olishini tekshiradi."""
        url = reverse('doctor-list')
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patient_can_list_doctors(self):
        """Bemor roli shifokorlar ro'yxatini ko'ra olishini tekshiradi."""
        url = reverse('doctor-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_retrieve_doctor(self):
        """Anonim foydalanuvchi bitta shifokor ma'lumotini ko'ra olishini tekshiradi."""
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(user=None)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_can_retrieve_doctor(self):
        """Autentifikatsiyadan o'tgan foydalanuvchi bitta shifokor ma'lumotini ko'ra olishini tekshiradi."""
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_cannot_create_doctor(self):
        """Anonim foydalanuvchi shifokor yarata olmasligini (401) tekshiradi."""
        url = reverse('doctor-list')
        self.client.force_authenticate(user=None)
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patient_cannot_create_doctor(self):
        """Bemor roli shifokor yarata olmasligini (403) tekshiradi."""
        url = reverse('doctor-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_doctor(self):
        """Admin roli yangi shifokor yarata olishini tekshiradi."""
        new_doctor_user = User.objects.create_user(username='doctor2', password='asdfg123', role='doctor')
        url = reverse('doctor-list')
        self.client.force_authenticate(self.admin_user)
        data = {
        'user': new_doctor_user.pk,
        'speciality': self.speciality.pk,
        'rank_type': self.rank_type.pk,
        'clinic': self.clinic.pk,
        'name_uz': 'Aziz',
        'name_ru': 'Азиз',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patient_cannot_delete_doctor(self):
        """Bemor roli shifokorni o'chira olmasligini (403) tekshiradi."""
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(self.patient_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_doctor(self):
        """Admin roli shifokorni o'chira olishini tekshiradi."""
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(self.admin_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_owner_doctor_can_update(self):
        """Profil egasi bo'lgan shifokor o'z ma'lumotini yangilay olishini tekshiradi."""
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(self.doctor_user)
        response = self.client.patch(url, {'bio_uz': 'Yangi bio'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_other_doctor_cannot_update(self):
        """Boshqa shifokor egasi bo'lmagan profilni yangilay olmasligini (403) tekshiradi."""
        other_doctor_user = User.objects.create_user(username='doctor3', password='qwerty456', role='doctor')
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(other_doctor_user)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patient_cannot_update_doctor(self):
        """Bemor roli shifokor profilini yangilay olmasligini (403) tekshiradi."""
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(self.patient_user)
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_any_doctor(self):
        """Admin roli istalgan shifokor profilini yangilay olishini tekshiradi."""
        url = reverse('doctor-detail', args=[self.doctor.pk])
        self.client.force_authenticate(self.admin_user)
        response = self.client.patch(url, {'bio_uz': 'Admin tomonidan yangilangan'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_can_list_doctor_schedules(self):
        """Autentifikatsiyadan o'tgan foydalanuvchi jadval ro'yxatini ko'ra olishini tekshiradi."""
        url = reverse('doctorschedule-list')
        self.client.force_authenticate(self.patient_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_can_create_own_schedule(self):
        """Shifokor o'zi uchun jadval yaratganda u avtomatik o'z profiliga bog'lanishini tekshiradi."""
        url = reverse('doctorschedule-list')
        self.client.force_authenticate(self.doctor_user)
        data = {'weekday': 0, 'start_time': '09:00', 'end_time': '18:00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        schedule = DoctorSchedule.objects.get(pk=response.data['id'])
        self.assertEqual(schedule.doctor_id, self.doctor.pk)

    def test_doctor_cannot_create_schedule_for_other_doctor(self):
        """Shifokor so'rovda boshqa shifokorni ko'rsatsa ham, jadval baribir o'zining profiliga bog'lanishini tekshiradi."""
        other_doctor_user = User.objects.create_user(username='doctor4', password='qwerty789', role='doctor')
        other_doctor = Doctor.objects.create(user=other_doctor_user, speciality=self.speciality, rank_type=self.rank_type, clinic=self.clinic, name_uz='Bekzod', name_ru='Бекзод')
        url = reverse('doctorschedule-list')
        self.client.force_authenticate(self.doctor_user)
        data = {'doctor': other_doctor.pk, 'weekday': 1, 'start_time': '09:00', 'end_time': '18:00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        schedule = DoctorSchedule.objects.get(pk=response.data['id'])
        self.assertEqual(schedule.doctor_id, self.doctor.pk)

    def test_duplicate_schedule_same_weekday_rejected(self):
        """Bir hafta kuni uchun ikkinchi marta jadval yaratish rad etilishini (400) tekshiradi."""
        DoctorSchedule.objects.create(doctor=self.doctor, weekday=0, start_time='09:00', end_time='18:00')
        url = reverse('doctorschedule-list')
        self.client.force_authenticate(self.doctor_user)
        data = {'weekday': 0, 'start_time': '10:00', 'end_time': '19:00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



