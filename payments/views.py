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
    permission_classes = [IsAuthenticated]

    def post(self, request):
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
    permission_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except (ValueError, stripe.error.SignatureVerificationError):
            return Response(status=400)

        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            payment = Payment.objects.filter(stripe_charge_id=intent['id']).first()
            if payment and payment.status != 'paid':
                payment.status = 'paid'
                payment.paid_at = timezone.now()
                payment.save()
                PaymentTransaction.objects.create(payment=payment, raw_data=event)

        return Response(status=200)

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated,IsAdmin]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()

        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)

        return queryset


class PaymentTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer




