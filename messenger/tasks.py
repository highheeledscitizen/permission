from .models import Message
from celery import shared_task
from django.core.serializers import serialize


@shared_task()
def log_last_ten_messages():
    last_messages = Message.objects.order_by('published_time')[:10]
    serialized_messages = serialize('json', last_messages)
    return serialized_messages
