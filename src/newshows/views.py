from django.shortcuts import render
from django.http import HttpResponse
from .helpers import updateTvMaze
from django.core.paginator import Paginator
from .models import Show

def index(request):
    return HttpResponse("Hello, world. You're at the new show index.")


def updateTVMaze(request):
    updateTvMaze()
    return HttpResponse("TVMaze Updated.")


def listShows(request):
    show_list = Show.objects.all()
    paginator = Paginator(show_list, 25) 

    page = request.GET.get('page')
    shows = paginator.get_page(page)
    return render(request, 'show_list.html', {'shows': shows})
