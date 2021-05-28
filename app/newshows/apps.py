import sys
from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "newshows"

    def ready(self):
        if not sys.argv[1] in [
            "makemigrations",
            "migrate",
            "loaddata",
            "collectstatic",
        ]:
            from .scheduler import start

            start()
