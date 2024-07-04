from celery import Celery
from django.conf import settings

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hw7.settings')

app = Celery(
    'hw7'
)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
