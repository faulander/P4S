from django.shortcuts import render
from django.http import HttpResponse
from .helpers import HelperUpdateTVMaze, HelperUpdateSonarr
from django.core.paginator import Paginator
from .models import Show
from django_tables2 import SingleTableView
from .tables import ShowTable
from .filters import ShowFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


def index(request):
    return HttpResponse("Hello, world. You're at the new show index.")


def updateTVMaze(request):
    HelperUpdateTVMaze()
    return HttpResponse("TVMaze Updated.")


def updateSonarr(request):
    HelperUpdateSonarr()
    return HttpResponse("Sonarr Updated.")


class FilteredShowListView(SingleTableMixin, FilterView):
    model = Show
    table_class = ShowTable
    template_name = 'show_list2.html'
    paginate_by = 35

    filterset_class = ShowFilter
