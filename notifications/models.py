from django.db import models

from users.models import User

class NotificationTemplate(models.Model):
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