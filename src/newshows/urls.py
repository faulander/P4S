
from . import views
from django.urls import path, include
from .views import FilteredShowListView, ShowViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'api_shows', views.ShowViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('', include(router.urls)),
    path('updateTVMaze/', views.updateTVMaze, name='updateTVMaze'),
    path('updateSonarr/', views.updateSonarr, name='updateSonarr'),
    path("shows/", FilteredShowListView.as_view()),
]
