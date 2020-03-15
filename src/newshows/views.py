
import logging
import json
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.urls import reverse
from .models import Show, Setting, Profile
from .tables import ShowTable
from .filters import ShowFilter

import requests
from extra_views import ModelFormSetView
from .helpers import getSonarrDownloads

logger = logging.getLogger(__name__)


# checked for 0.2.0
def addShowToSonarr(request):
    """
    Info from Sonarr:
    Required: tvdbId (int) title (string) profileId (int) titleSlug (string) images (array) seasons (array)
    See GET output for format
    """
    settings = Setting.load()
    thetvdb_id = request.GET.get('thetvdb_id', None)
    logger.info("Trying {}".format(thetvdb_id))
    newshowdict = dict()
    if not settings.SONARR_ROOTFOLDER:
        url = settings.SONARR_URL + "/rootfolder/?apikey=" + settings.SONARR_APIKEY
        logger.info("Trying {}".format(url))
        r = requests.get(url)
        statuscode = r.status_code
        if statuscode == 200:  # Show has been found
            ret = r.json()
            settings.SONARR_ROOTFOLDER = ret[0]["path"]
            logger.info("Rootfolder set to {}".format(settings.SONARR_ROOTFOLDER))
            settings.save()
        else:
            logger.error("Couldn't get rootfolder from Sonarr.")
            data = {'status': False}
            return JsonResponse(data)
    url = settings.SONARR_URL + "/series/lookup?term=tvdb:" + str(thetvdb_id) + "&apikey=" + settings.SONARR_APIKEY
    logger.info("Trying {}".format(url))
    r = requests.get(url)
    statuscode = r.status_code
    if statuscode == 200:  # Show has been found
        r = r.json()
        newshowdict['tvdbId'] = int(thetvdb_id)
        newshowdict['title'] = r[0]['title']
        tmpP = Profile.objects.get(pk=int(s.profile_id))
        newshowdict['profileId'] = tmpP.profile_id
        newshowdict['titleSlug'] = r[0]['titleSlug']
        newshowdict['images'] = r[0]['images']
        newshowdict['seasons'] = r[0]['seasons']
        newshowdict['rootFolderPath'] = settings.SONARR_ROOTFOLDER
        newshowdict['monitored'] = bool(s.addmonitored)
        newshowdict['seasonFolder'] = bool(s.seasonfolders)
        newshow = json.dumps(newshowdict)
        print(newshow)
        url = settings.SONARR_URL + "/series?apikey=" + settings.SONARR_APIKEY
        logger.info("Trying {}".format(url))
        r = requests.post(url, data=newshow)
        logger.info("Status: {}".format(r.status_code))
        if r.status_code == 201:
            logger.info("Show {} added to Sonarr".format(newshowdict['title']))
            data = {'status': 1}
            #  Update local DB
            currShow = Show.objects.get(thetvdb_id=int(thetvdb_id))
            currShow.insonarr = True
            currShow.save()
            logger.info("Show {} updated in local DB".format(newshowdict['title']))
            data = {'status': 1, 'show': newshowdict['title']}
            return JsonResponse(data)
        else:
            logger.error("Adding of Show {} to Sonarr failed".format(newshowdict['title']))
            data = {'status': 0, 'show': newshowdict['title']}
            return JsonResponse(data)
    else:
        logger.error("Lookup in Sonarr failed")
        data = {'status': 0, 'show': newshowdict['title']}
        return JsonResponse(data)

# checked for 0.2.0
def lastSonarrDownloads(request):
    try:
        status, lastDownloads = getSonarrDownloads()
        return render(request, 'downloads.html', {"data": lastDownloads})
    except:
        raise Http404("History couldn't be loaded.")

# checked for 0.2.0
class FilteredShowListView(SingleTableMixin, FilterView):
    model = Show
    table_class = ShowTable
    template_name = 'show.html'
    paginate_by = 35

    filterset_class = ShowFilter

# checked for 0.2.0
class SettingsFormSetView(UpdateView):
    model = Setting
    fields = ['SONARR_URL', 'SONARR_APIKEY', 'profile', 'addmonitored', 'seasonfolders']
    template_name = 'settings.html'

    def get_object(self):
        return Setting.objects.get(pk=1)

    def get_success_url(self):
        return reverse('shows')
    
    def form_invalid(self, form):
        logger.error(form)