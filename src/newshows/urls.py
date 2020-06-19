
from django.urls import path
from django.conf import settings
from .views import FilteredShowListView, SettingsFormSetView
from . import views

urlpatterns = [
    path('', FilteredShowListView.as_view(), name="shows"),
    path("shows/", FilteredShowListView.as_view()),
    path("settings/", SettingsFormSetView.as_view(), name='settings'),
    path('addShowToSonarr/', views.addShowToSonarr, name='addShowToSonarr'),
    path("downloads/", views.lastSonarrDownloads, name='lastSonarrDownloads'),
]

# checked for 0.2.0
