import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'practice.settings')

app = Celery('practice')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scraping-task': {
        'task': 'quote.tasks.quote_task',

    }
}
