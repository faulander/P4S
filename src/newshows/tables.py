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
        if record.imdb_id:
            return format_html("{}<br/> <a href='https://www.imdb.com/title/{}'>IMDB</a>", value, record.imdb_id)
        else:
            return format_html("{}", value)
   
    def render_insonarr(self, value, record):
        if record.thetvdb_id and not value:
            return format_html("<a href='http://test/{}'>{}</a>", record.thetvdb_id, value)
        else:
            return value
