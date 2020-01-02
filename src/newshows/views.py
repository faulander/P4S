#  from django.shortcuts import render
from django.http import HttpResponse
from .helpers import HelperUpdateTVMaze, HelperUpdateSonarr
#  from django.core.paginator import Paginator
from .models import Show
#  from django_tables2 import SingleTableView
from .tables import ShowTable
from .filters import ShowFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
#  from rest_framework import viewsets
#  from .serializers import ShowSerializer
#  from .pagination import CustomPagination
import requests
from loguru import logger

def AddShowToSonarr(request, thetvdb_id):
    """
    try:
        sonarr_url = Settings.objects.values_list('value', flat=True).get(setting="sonarr_url")  
        sonarr_apikey = Settings.objects.values_list('value', flat=True).get(setting="sonarr_apikey")
    except:
        return False
    endpoint = "/series"
    url = sonarr_url + endpoint + "?apikey=" + sonarr_apikey
    logger.debug("Trying {}", url)
    r = requests.post(url)
    statuscode = r.status_code
    """
    logger.debug(thetvdb_id)    


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

"""
class ShowViewSet(viewsets.ModelViewSet):
    API endpoint that allows Shows to be viewed or edited.
    queryset = Show.objects.all().order_by('-premiere')
    serializer_class = ShowSerializer
    pagination_class = CustomPagination
"""