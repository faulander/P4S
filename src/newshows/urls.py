
from . import views
from django.urls import path, include
from .views import FilteredShowListView

urlpatterns = [
    path('', views.index, name='index'),
    #  path('', include(router.urls)),
    path('updateTVMaze/', views.updateTVMaze, name='updateTVMaze'),
    path('updateSonarr/', views.updateSonarr, name='updateSonarr'),
    path("shows/", FilteredShowListView.as_view()),
    path("api/<int:thetvdb_id>", views.AddShowToSonarr, name='addShowToSonarr'),
    path('settings/', views.UpdateSettings.as_view()),

]

