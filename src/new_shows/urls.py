from django.contrib import admin
from django.urls import path, include
from newshows import helpers
import os

urlpatterns = [
    path('', include('newshows.urls')),
    path('admin/', admin.site.urls),
]

if not os.environ['firstrun']:
    # Run the Updater once on Startup
    helpers.HelperUpdateTVMaze()
    helpers.HelperUpdateShows()
    os.environ['firstrun'] = "1"
