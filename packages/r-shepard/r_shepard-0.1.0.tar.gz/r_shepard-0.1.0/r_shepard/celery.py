import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "r_shepard.settings")

app = Celery("r_shapard")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
