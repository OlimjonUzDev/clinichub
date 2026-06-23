from django.db import models

class MessageTemplate(models.Model):
    TRIGGER_CHOICES = (
        ('appointment_created', 'Appointment Created'),
        ('status_changed', 'Status Changed'),
        ('reminder', 'Reminder')
    )
    trigger_type = models.CharField(max_length=225, choices=TRIGGER_CHOICES)
    template_text = models.TextField()

    def __str__(self):
        return self.trigger_type
