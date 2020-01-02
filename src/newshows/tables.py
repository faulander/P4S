# tutorial/tables.py
import django_tables2 as tables
from .models import Show
from django.utils.html import format_html


class ShowTable(tables.Table):
    # Edit = tables.TemplateColumn('<input type="checkbox" value="{{ record.pk }}" />', verbose_name="Edit")

    class Meta:
        model = Show
        fields = ("name", "network", "webchannel", "genre", "language", "status", "premiere", "insonarr",)


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
        if record.thetvdb_id and not value:
            return format_html("<a href='/api/{}'>Add to Sonarr</a>", record.thetvdb_id)
        elif not record.thetvdb_id:
            return "No ID"
