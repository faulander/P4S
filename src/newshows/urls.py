
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('updateTVMaze/', views.updateTVMaze, name='updateTVMaze'),
    path('list/', views.listShows, name='listshows')

]
