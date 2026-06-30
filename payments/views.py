from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment, PaymentTransaction
from .serializers import PaymentSerializer, PaymentTransactionSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        queryset = Payment.objects.all()

        # GET /api/v1/payments/payment/?patient_id=8
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)

        # GET /api/v1/payments/payment/?invoice_id=3
        invoice_id = self.request.query_params.get('invoice_id')
        if invoice_id:
            queryset = queryset.filter(invoice_id=invoice_id)

        return queryset


class PaymentTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [IsAdmin]
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer


# --- Webhook Views ---
# To'lov tizimlari shu endpointlarga POST so'rov yuboradi

class PaymeCallbackView(APIView):
    def post(self, request):
        method = request.data.get('method', '')
        params = request.data.get('params', {})
        transaction_id = str(params.get('id', ''))

        payment = Payment.objects.filter(transaction_id=transaction_id).first()

        if payment:
            # Kelgan ma'lumotni logga yozamiz
            PaymentTransaction.objects.create(payment=payment, raw_data=request.data)

            # To'lov tasdiqlansa statusni yangilaymiz
            if method == 'PerformTransaction':
                payment.status = 'paid'
                payment.paid_at = timezone.now()
                payment.save()

        return Response({'result': {'transaction': transaction_id}})


class ClickCallbackView(APIView):
    def post(self, request):
        payment_id    = request.data.get('merchant_trans_id')
        click_trans_id = request.data.get('click_trans_id')
        action        = request.data.get('action')
        error         = request.data.get('error')

        payment = Payment.objects.filter(id=payment_id).first()
        if not payment:
            return Response({'error': -5, 'error_note': "To'lov topilmadi"}, status=404)

        # Kelgan ma'lumotni logga yozamiz
        PaymentTransaction.objects.create(payment=payment, raw_data=request.data)

        # action=1 va error=0 bo'lsa — to'lov muvaffaqiyatli
        if action == 1 and error == 0:
            payment.status = 'paid'
            payment.transaction_id = str(click_trans_id)
            payment.paid_at = timezone.now()
            payment.save()

        return Response({'error': 0, 'error_note': 'Success'})


class UzumCallbackView(APIView):
    def post(self, request):
        order_id       = request.data.get('order_id')
        transaction_id = request.data.get('transaction_id')
        uzum_status    = request.data.get('status')

        payment = Payment.objects.filter(id=order_id).first()
        if not payment:
            return Response({'message': "To'lov topilmadi"}, status=404)

        # Kelgan ma'lumotni logga yozamiz
        PaymentTransaction.objects.create(payment=payment, raw_data=request.data)

        if uzum_status == 'CONFIRMED':
            payment.status = 'paid'
            payment.transaction_id = transaction_id
            payment.paid_at = timezone.now()
            payment.save()

        return Response({'message': 'OK'})
