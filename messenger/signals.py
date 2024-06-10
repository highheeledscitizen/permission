from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, LogEntry


@receiver(pre_save, sender=Message)
def add_log_entry(sender, instance,   **kwargs):
    if instance.author.is_superuser:
        role = 'SUPER'
    else:
        role = 'SIMPLE'
    log = LogEntry(action=role + ' USER POSTED: ' + instance.text,
                   author=instance.author)
    log.save()
