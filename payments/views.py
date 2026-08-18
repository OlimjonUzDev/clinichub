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

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),
                currency='usd',
                metadata={'payment_id': payment.id},
            )
        except stripe.error.StripeError:
            return Response({'error': "To'lov tizimida xatolik yuz berdi, birozdan so'ng qayta urinib ko'ring"}, status=502)

        payment.stripe_charge_id = intent.id
        payment.save()
        return Response({'client_secret': intent.client_secret})

@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    permission_classes = []

    def post(self, request):
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
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
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
        if self.action in ['list', 'create', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdmin()]


class PaymentTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer




