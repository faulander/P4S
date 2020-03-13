import os
import logging
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from newshows.models import Setting

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Gets the initial show data from TVMaze'

    def handle(self, *args, **kwargs):
        sonarr = checkForActiveSonarr(SONARR_URL, SONARR_APIKEY)
        if sonarr:
            self.stdout.write(self.style.SUCCESS('Successfully connected to Sonarr'))
        else:
            raise CommandError("Connecting to Sonarr failed. Please doublecheck your environment variables SONARR_URL and SONARR_APIKEY")

        if os.path.isfile(os.path.join(BASE_DIR, ".firstrun.done")):
            logger.info("It's not the first run of P4S.")
        else:
            logger.info("Empty db found.")
            if "newshows_show" in connection.introspection.table_names() and Setting.objects.filter(pk=1).exists():
                logger.info("Initial Setup starting.")
                HelperUpdateTVMaze()
                f = open(os.path.join(BASE_DIR, ".firstrun.done"), 'w')
                f.write("Firstrun done.")
                f.close()
            else:
                logger.error("No Firstrun done, passing.")
