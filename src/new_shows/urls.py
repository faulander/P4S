from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.staticfiles import views
from django.urls import re_path


urlpatterns = [
    path('', include('newshows.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()

