import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lead_magnet.settings")

app = Celery("lead_magnet")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
