from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentViewSet,
    PaymentTransactionViewSet,
    CreateStripeIntentView,
    StripeWebhookView,
)

router = DefaultRouter()
router.register(r'payment', PaymentViewSet)
router.register(r'transaction', PaymentTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stripe/create-intent/', CreateStripeIntentView.as_view(), name='stripe-create-intent'),
    path('webhook/stripe/', StripeWebhookView.as_view(), name='stripe-webhook'),
]
