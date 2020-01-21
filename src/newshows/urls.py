
from . import views
from django.urls import path
from django.conf import settings
from .views import FilteredShowListView, SettingsFormSetView

urlpatterns = [
    path('', FilteredShowListView.as_view()),
    path("shows/", FilteredShowListView.as_view()),
    path("settings/", SettingsFormSetView.as_view()),
    path('addShowToSonarr/', views.addShowToSonarr, name='addShowToSonarr'),
    path("downloads/", views.lastSonarrDownloads, name='lastSonarrDownloads'),
]
