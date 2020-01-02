from django.contrib import admin
from django.urls import path, include
from newshows import helpers

urlpatterns = [
    path('', include('newshows.urls')),
    path('admin/', admin.site.urls),
]
