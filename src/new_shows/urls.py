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

getSonarrDownloads(repeat=60, repeat_until=None)
checkForActiveSonarr(repeat=60, repeat_until=None)
HelperUpdateSonarr(repeat=300, repeat_until=None)
HelperUpdateTVMaze(repeat=180, repeat_until=None)
HelperUpdateShows(repeat=10800, repeat_until=None)
helperGetSonarrProfiles(repeat=360, repeat_until=None)