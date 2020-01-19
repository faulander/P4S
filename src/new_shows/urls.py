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
