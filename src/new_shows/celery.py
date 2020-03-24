
import os
import logging
from celery import Celery
from celery import signals

logger = logging.getLogger(__name__)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_shows.settings')
app = Celery('new_shows')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@signals.setup_logging.connect
def on_celery_setup_logging(**kwargs):
    pass