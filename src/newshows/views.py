from django.shortcuts import render
from django.http import HttpResponse
from .helpers import updateTvMaze

def index(request):
    return HttpResponse("Hello, world. You're at the new show index.")

def updateTVMaze(request):
    updateTvMaze()
    return HttpResponse("TVMaze Updated.")