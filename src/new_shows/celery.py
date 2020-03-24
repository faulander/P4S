
import os
import logging
from loguru import logger
from celery import Celery
from celery.signals import setup_logging
from celery.signals import after_setup_logger

class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_shows.settings')
app = Celery('new_shows')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@after_setup_logger.connect
def on_celery_setup_logging(logger=None, loglevel=logging.DEBUG, **kwargs):
    handler = InterceptHandler()
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


logging.basicConfig(handlers=[InterceptHandler()], level=0)
