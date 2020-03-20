from django.contrib import admin
from django.urls import path, include
from newshows import helpers
import os
import sys
from django.conf import settings
from newshows.models import Show, Setting
from django.db import connection
import logging
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles import views
from django.urls import re_path
from newshows.helpers import getSonarrDownloads, checkForActiveSonarr, HelperUpdateSonarr
from newshows.helpers import HelperUpdateTVMaze, HelperUpdateShows, helperGetSonarrProfiles

logger = logging.getLogger(__name__)

urlpatterns = [
    path('', include('newshows.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()

huey_logger = logging.getLogger("huey")
if huey_logger.handlers:
    logger.info(
        f"Handlers of huey_logger (before removing huey default handler): {huey_logger.handlers}"
    )
    huey_logger.handlers.pop()
    logger.info(
        f"Handlers of huey_logger (after removing huey default handler): {huey_logger.handlers}"
    )
    huey_logger.info("This should not appear.")

