import logging
import logging
from django.utils.html import format_html
from django.conf import settings
from django.contrib.staticfiles import finders
from .models import Show, Setting
import django_tables2 as tables
from django.templatetags.static import static

logger = logging.getLogger(__name__)

# checked for 0.2.0
class ShowTable(tables.Table):
    # Edit = tables.TemplateColumn('<input type="checkbox" value="{{ record.pk }}" />', verbose_name="Edit")
    premiere = tables.DateColumn(format="y-m-d")

    class Meta:
        model = Show
        fields = (
            "name",
            "network",
            "webchannel",
            "genre",
            "language",
            "status",
            "premiere",
            "insonarr",
        )

    def render_name(self, value, record):

        returnstring = ""
        if record.tvmaze_id:
            returnstring += (
                "<a href='https://www.tvmaze.com/shows/"
                + str(record.tvmaze_id)
                + "'><img src='"
                + static("img/tvmaze.ico")
                + "'"
                + " height='20px'></a>"
            )

        if record.imdb_id:
            returnstring += (
                "<a href='https://www.imdb.com/title/"
                + str(record.imdb_id)
                + "'><img src='"
                + static("img/imdb.ico")
                + "'"
                + " height='20px'></a>"
            )

        returnstring = "<strong>" + value + "</strong><br />" + returnstring

        return format_html(returnstring)

    def render_insonarr(self, value, record):
        if record.thetvdb_id and not value:
            returnstring = (
                "<button class='btn btn-primary addSonarr' value='"
                + str(record.thetvdb_id)
                + "' name='btn_addSonarr'>Add</button>"
            )
            return format_html(returnstring)
        elif not record.thetvdb_id:
            returnstring = (
                "<button class='btn btn-secondary lookupSonarr' value='"
                + str(record.name)
                + "' name='btn_addSonarr'>Lookup</button>"
            )
            return format_html(returnstring)
