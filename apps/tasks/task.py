import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_study.settings")

app = Celery(
    'celery',
    broker="redis://@localhost:32769/4"
)

app.config_from_object(
    "apps.tasks.celery_config", silent=True
)
