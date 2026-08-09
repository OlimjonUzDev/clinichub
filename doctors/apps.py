from django.apps import AppConfig


class DoctorsConfig(AppConfig):
    """"doctors" ilovasining konfiguratsiyasini belgilaydi."""

    name = 'doctors'

    def ready(self):
        """Ilova tayyor bo'lganda signallar modulini ro'yxatdan o'tkazish uchun import qiladi."""
        import doctors.signals
