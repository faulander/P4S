from django.contrib import admin
from django.urls import path, include
from newshows import helpers
import os
from django.conf import settings
from newshows.models import Show, Setting
from django.db import connection
import logging


logger = logging.getLogger(__name__)

urlpatterns = [
    path('', include('newshows.urls')),
    path('admin/', admin.site.urls),
]

try:
    f = open(".firstrun.done")
except FileNotFoundError:
    if "newshows_show" in connection.introspection.table_names() and Setting.objects.filter(pk=1).exists():
        logger.info("Initial Setup starting.")
        helpers.threadHelperUpdateTVMaze()
        #helpers.HelperUpdateTVMaze()
        #helpers.HelperUpdateShows()
        #helpers.HelperUpdateSonarr()

