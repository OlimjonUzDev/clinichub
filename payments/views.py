import stripe
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Payment, PaymentTransaction
from .serializers import PaymentSerializer, PaymentTransactionSerializer
from users.permissions import IsAdmin

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateStripeIntentView(APIView):
    """Autentifikatsiyadan o'tgan foydalanuvchi uchun o'ziga tegishli to'lov bo'yicha Stripe PaymentIntent yaratadi."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """So'rovda kelgan payment_id bo'yicha Stripe PaymentIntent yaratib, client_secret qaytaradi.

        Faqat so'rov yuborgan foydalanuvchiga tegishli to'lov uchun ishlaydi.

        Parametrlar:
            request: Tarkibida 'payment_id' bo'lgan HTTP so'rov.

        Qaytaradi:
            Response: Muvaffaqiyatda {'client_secret': ...}, to'lov
            topilmasa 404 statusi bilan xabar.
        """
        payment_id = request.data.get('payment_id')
        payment = Payment.objects.filter(id=payment_id, patient__user=request.user).first()
        if not payment:
            return Response({'error': "To'lov topilmadi"}, status=404)

        intent = stripe.PaymentIntent.create(
            amount=int(payment.amount * 100),  # Stripe tiyin/cent bilan ishlaydi
            currency='usd',                     # UZS Stripe'da yo'q, shu sabab hozircha USD
            metadata={'payment_id': payment.id},
        )
        payment.stripe_charge_id = intent.id
        payment.save()
        return Response({'client_secret': intent.client_secret})


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    """Stripe dan keladigan webhook eventlarini qabul qiladigan, ruxsatsiz (public) endpoint."""

    permission_classes = []

    def post(self, request):
        """Stripe webhook imzosini tekshiradi va 'payment_intent.succeeded' eventida to'lovni "paid" qiladi.

        To'lov muvaffaqiyatli bo'lganda Payment statusi va paid_at
        yangilanadi hamda webhook logi PaymentTransaction sifatida
        saqlanadi.

        Parametrlar:
            request: Stripe tomonidan yuborilgan xom (raw) webhook so'rovi.

        Qaytaradi:
            Response: Imzo noto'g'ri bo'lsa 400, webhook maxfiy kaliti
            sozlanmagan bo'lsa 503, aks holda 200 statusi.
        """
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        if not webhook_secret:
            return Response(status=503)

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=400)

        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            payment = Payment.objects.filter(stripe_charge_id=intent['id']).first()
            if payment and payment.status != 'paid':
                payment.status = 'paid'
                payment.paid_at = timezone.now()
                payment.save()
                PaymentTransaction.objects.create(payment=payment, raw_data=event.to_dict())

        return Response(status=200)

class PaymentViewSet(viewsets.ModelViewSet):
    """To'lovlar (Payment) uchun CRUD endpointlari.

    Oddiy foydalanuvchilar faqat o'ziga tegishli to'lovlarni ko'ra oladi,
    admin barcha to'lovlarni boshqara oladi (list/create/retrieve uchun
    autentifikatsiya, boshqa amallar uchun admin huquqi talab qilinadi).
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        """Foydalanuvchi roli va query parametrlarga (patient_id, invoice_id) mos to'lovlar ro'yxatini qaytaradi.

        Admin bo'lmagan foydalanuvchilar uchun faqat o'ziga tegishli
        to'lovlar bilan cheklanadi.

        Qaytaradi:
            QuerySet: Filtrlangan Payment obyektlari.
        """
        queryset = Payment.objects.all()
        user = self.request.user
        if user.role != 'admin':
            queryset = queryset.filter(patient__user=user)

        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)
        return queryset

    def get_permissions(self):
        """Amal turiga qarab kerakli ruxsat sinflarini qaytaradi.

        list/create/retrieve uchun oddiy autentifikatsiya, qolgan
        amallar (update/delete va h.k.) uchun admin huquqi talab qilinadi.

        Qaytaradi:
            list: Amal uchun qo'llaniladigan permission obyektlari ro'yxati.
        """
        if self.action in ['list', 'create', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin()]


class PaymentTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """Faqat admin uchun ochiq, PaymentTransaction (webhook loglari) ni faqat o'qish uchun ko'rsatadigan endpoint."""

    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer




