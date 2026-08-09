from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    """Payments ilovasining Django konfiguratsiyasi."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payments'

    def ready(self):
        """Ilova ishga tushganda signal handlerlarni ro'yxatdan o'tkazish uchun signals modulini import qiladi."""
        import payments.signals
