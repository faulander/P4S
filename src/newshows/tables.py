# tutorial/tables.py
import django_tables2 as tables
from .models import Show
from django.utils.html import format_html


class ShowTable(tables.Table):
    class Meta:
        model = Show
        # template_name = "django_tables2/bootstrap.html"
        fields = ("name", "network", "webchannel", "genre", "language", "status", "premiere", "insonarr", "ignored", )

    def render_name(self, value, record):
        if record.imdb_id:
            return format_html("{}<br/> <a href='https://www.imdb.com/title/{}'>IMDB</a>", value, record.imdb_id)
        else:
            return format_html("{}", value)
   