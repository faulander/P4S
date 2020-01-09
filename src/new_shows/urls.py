from django.contrib import admin
from django.urls import path, include
from newshows import helpers
import os
from django.conf import settings
from newshows.models import Show

urlpatterns = [
    path('', include('newshows.urls')),
    path('admin/', admin.site.urls),
]

try:
    f = open(".firstrun.done")
except FileNotFoundError:
    helpers.HelperUpdateTVMaze()
    helpers.HelperUpdateShows()
    helpers.HelperUpdateSonarr()
    #  Firstrun isn't done
    f = open(".firstrun.done","w+")
    f.write("Firstrun done.")
    f.close()

