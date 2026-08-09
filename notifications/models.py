from django.db import models

from users.models import User

class NotificationTemplate(models.Model):
    """Xabarnoma matnining shabloni (SMS, email yoki push uchun).

    `name` shablon nomini, `body_uz`/`body_ru` esa xabar matnini o'zbek va
    rus tillarida saqlaydi. `type` maydoni shablon qaysi kanal (sms/email/
    push) uchun ekanligini `STATUS_CHOICES` orqali belgilaydi.
    """

    STATUS_CHOICES = (
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('push', 'Push')
    )
    name = models.CharField(max_length=225)
    body_uz = models.TextField()
    body_ru = models.TextField()
    type = models.CharField(max_length=225, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class NotificationLog(models.Model):
    """Foydalanuvchiga yuborilgan (yoki yuborilishi kerak bo'lgan) xabarnoma yozuvi.

    Har bir yozuv qaysi `NotificationTemplate` asosida, qaysi `User`ga,
    qanday matn (`message`) va qaysi kanal (`type`) orqali yuborilganini,
    shuningdek yuborilganlik holati (`is_sent`) va vaqtini (`sent_at`,
    `created_at`) saqlaydi.
    """

    STATUS_CHOICES = (
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('push', 'Push')
    )
    template = models.ForeignKey(NotificationTemplate,on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.CharField(max_length=225, choices=STATUS_CHOICES)
    is_sent = models.BooleanField(default=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)