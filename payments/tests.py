from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Payment, PaymentTransaction
from patients.models import Patient
from billing.models import Invoice

User = get_user_model()

class PaymentsViewSetTestCase(APITestCase):

    def setUp(self):
        pass