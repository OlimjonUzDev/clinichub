from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    PaymentViewSet,
    PaymentTransactionViewSet,
    PaymeCallbackView,
    ClickCallbackView,
    UzumCallbackView,
)

router = DefaultRouter()
router.register(r'payment', PaymentViewSet)
router.register(r'transaction', PaymentTransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Webhook endpointlar — har bir to'lov tizimi uchun alohida
    path('webhook/payme/', PaymeCallbackView.as_view(), name='payme-webhook'),
    path('webhook/click/', ClickCallbackView.as_view(), name='click-webhook'),
    path('webhook/uzum/', UzumCallbackView.as_view(), name='uzum-webhook'),
]
