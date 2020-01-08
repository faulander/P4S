from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Show, Setting
from .tables import ShowTable
from .filters import ShowFilter
from .forms import SettingForm

import requests
import logging

logger = logging.getLogger(__name__)


def AddShowToSonarr(request, thetvdb_id):
    """
    Info from Sonarr:
    Required: tvdbId (int) title (string) profileId (int) titleSlug (string) images (array) seasons (array) - See GET output for format

    TODO: get ProfileId's
    TODO: get title
    TODO: create titleSlug
    TODO: Create ImageArray
    TODO: Get seasons 
    
    meanwhile use Lookup, endpoint /series/lookups
    
    """
    try:
        sonarr_url = Settings.objects.values_list('value', flat=True).get(setting="sonarr_url")  
        sonarr_apikey = Settings.objects.values_list('value', flat=True).get(setting="sonarr_apikey")
    except:
        return False
    endpoint = "/series/lookup"
    url = sonarr_url + endpoint + "?term=tvdb:" + str(thetvdb_id) + "&?apikey=" + sonarr_apikey
    logger.debug("Trying {}", url)
    r = requests.post(url)
    statuscode = r.status_code
    if statuscode == 200:
        pass
    else:
        return False


def index(request):
    return HttpResponse("Hello, world. You're at the new show index.")


class FilteredShowListView(SingleTableMixin, FilterView):
    model = Show
    table_class = ShowTable
    template_name = 'show_list2.html'
    paginate_by = 35

    filterset_class = ShowFilter


class UpdateSettings(SuccessMessageMixin, UpdateView):
    model = Setting
    form_class = SettingForm
    template_name = 'settings.html'
    success_message = "Settings saved"

    def get_object(self):
        return Setting.objects.get(pk=1)