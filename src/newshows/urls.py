
from . import views
from django.urls import path
from .views import FilteredShowListView, SettingsFormSetView

urlpatterns = [
    path('', FilteredShowListView.as_view()),
    path("shows/", FilteredShowListView.as_view()),
    path("api/<int:thetvdb_id>", views.AddShowToSonarr, name='addShowToSonarr'),
    path("settings/", SettingsFormSetView.as_view()),

]
