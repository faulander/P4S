# tutorial/tables.py
import django_tables2 as tables
from .models import Show, Setting
from django.utils.html import format_html
from django.conf import settings


class ShowTable(tables.Table):
    # Edit = tables.TemplateColumn('<input type="checkbox" value="{{ record.pk }}" />', verbose_name="Edit")
    premiere = tables.DateColumn(format="y-m-d")

    class Meta:
        model = Show
        fields = ("name", "network", "webchannel", "genre", "language", "status", "premiere")
        if settings.SONARR_OK:
            fields += ("insonarr",)


    def render_name(self, value, record):
        returnstring = ""
        if record.tvmaze_id:
            returnstring += "<a href='https://www.tvmaze.com/show/" + str(record.tvmaze_id) + "'><img src='/static/img/tvmaze.ico' height='20px'></a>" 
        if record.imdb_id:
            returnstring += "<a href='https://www.imdb.com/title/" + record.imdb_id + "'><img src='/static/img/imdb.ico' height='20px'></a>" 
        if record.tvrage_id:
            returnstring += "<a href='http://www.tvrage.com/search/?search=" + record.tvrage_id + "'><img src='/static/img/tvrage.ico' height='20px'></a>"
        if record.thetvdb_id:
            returnstring += "<a href='https://thetvdb.com/search?query=" + record.thetvdb_id + "'><img src='/static/img/thetvdb.ico' height='20px'></a>"
        returnstring = "<strong>" + value + "</strong><br />" + returnstring
        return format_html(returnstring)


    def render_insonarr(self, value, record):
        if settings.SONARR_OK:
            if record.thetvdb_id and not value:
                returnstring = "<button class='btn btn-primary' id='addSonarr' value='" + str(record.thetvdb_id) + "' name='btn_addSonarr'>Add</button>"
                return format_html(returnstring)
            elif not record.thetvdb_id:
                returnstring = "<button class='btn btn-secondary' id='lookupSonarr' value='" + str(record.name) + "' name='btn_addSonarr'>Lookup</button>"
                return format_html(returnstring)
