from django.apps import AppConfig


class AppointmentsConfig(AppConfig):
    """Appointments ilovasining Django konfiguratsiyasi."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appointments'

    def ready(self):
        """Ilova ishga tushganda signal handlerlarni ro'yxatdan o'tkazadi."""
        import appointments.signals
