from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Show, Setting
from .tables import ShowTable
from .filters import ShowFilter
from django.conf import settings

import requests
import logging
import json
from extra_views import ModelFormSetView

logger = logging.getLogger(__name__)

def AddShowToSonarr(request, thetvdb_id):
    """
    Info from Sonarr:
    Required: tvdbId (int) title (string) profileId (int) titleSlug (string) images (array) seasons (array) - See GET output for format
    """
    newshowdict = dict()
    url = settings.SONARR_URL + "/rootfolder&?apikey=" + settings.SONARR_APIKEY
    logger.debug("Trying {}", url)
    r = requests.get(url)
    statuscode = r.status_code
    if statuscode == 200:  # Show has been found
        rootpath = r['path']
    else:
        return json.dump(False)
    url = settings.sonarr_url + "/series/lookup?term=tvdb:" + str(thetvdb_id) + "&?apikey=" + settings.sonarr_apikey
    logger.debug("Trying {}", url)
    r = requests.get(url)
    statuscode = r.status_code
    if statuscode == 200:  # Show has been found
        newshowdict['title'] = r['title']
        newshowdict['profileId'] = r['profileId']
        newshowdict['titleSlug'] = r['titleSlug']
        newshowdict['seasons'] = r['seasons']
        newshowdict['images'] = r['images']
        newshowdict['rootFolderPath'] = rootpath
        newshowdict['monitored'] = True
        newshow = json.dump(newshowdict)
        url = settings.sonarr_url + "/series&?apikey=" + settings.sonarr_apikey
        logger.debug("Trying {}", url)
        r = requests.post(url, newshow)
        if r.statuscode == 200:
            return json.dump(True)
        else:
            return json.dump(False)
    else:
        return json.dump(False)


class FilteredShowListView(SingleTableMixin, FilterView):
    model = Show
    table_class = ShowTable
    template_name = 'show.html'
    paginate_by = 35

    filterset_class = ShowFilter


class SettingsFormSetView(ModelFormSetView):
    model = Setting
    fields = ['profile']
    template_name = 'settings.html'
    factory_kwargs = {'extra': 0}

