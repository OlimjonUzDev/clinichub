from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NotificationTemplateViewSet, NotificationLogViewSet

router = DefaultRouter()
router.register(r'message_template', NotificationTemplateViewSet)
router.register(r'notificationlog', NotificationLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


