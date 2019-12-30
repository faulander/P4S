
from . import views
from django.urls import path
from .views import FilteredShowListView

urlpatterns = [
    path('', views.index, name='index'),
    path('updateTVMaze/', views.updateTVMaze, name='updateTVMaze'),
    path("shows/", FilteredShowListView.as_view()),


]
