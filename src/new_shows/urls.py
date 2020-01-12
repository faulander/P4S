from django.contrib import admin
from django.urls import path, include
from newshows import helpers
import os
import sys
from django.conf import settings
from newshows.models import Show, Setting
from django.db import connection
import logging


logger = logging.getLogger(__name__)

urlpatterns = [
    path('', include('newshows.urls')),
    path('admin/', admin.site.urls),
]

settings.SONARR_OK = helpers.checkForActiveSonarr(settings.SONARR_URL, settings.SONARR_APIKEY)

if not settings.SONARR_OK:
    sys.exit("Connection to Sonarr failed.")

if os.path.isfile(".firstrun.done"):
    logger.info("It's not the first run of P4S.")
else:
    logger.info("Empty db found.")
    if "newshows_show" in connection.introspection.table_names() and Setting.objects.filter(pk=1).exists():
        logger.info("Initial Setup starting.")
        helpers.HelperUpdateTVMaze()
        # helpers.HelperUpdateShows()
        # helpers.HelperUpdateSonarr()
        f = open(".firstrun.done", 'w')
        f.write("Firstrun done.")
        f.close()
    else:
        logger.error("No Firstrun done, passing.")
