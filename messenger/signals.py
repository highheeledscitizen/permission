from django.db.models.signals import pre_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import Message, LogEntry, UserStatus


@receiver(pre_save, sender=Message)
def add_log_entry(sender, instance,   **kwargs):
    if instance.author.is_superuser:
        role = 'SUPER'
    else:
        role = 'SIMPLE'
    log = LogEntry(action=role + ' USER POSTED: ' + instance.text,
                   author=instance.author)
    log.save()


@receiver(user_logged_in)
def user_logged_in_handler(sender, request, user, **kwargs):
    status, created = UserStatus.objects.get_or_create(user=user)
    status.online = True
    status.save()


@receiver(user_logged_out)
def user_logged_out_handler(sender, request, user, **kwargs):
    status, created = UserStatus.objects.get_or_create(user=user)
    status.online = False
    status.save()
