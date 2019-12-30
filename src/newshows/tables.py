# tutorial/tables.py
import django_tables2 as tables
from .models import Show


class ShowTable(tables.Table):
    class Meta:
        model = Show
        # template_name = "django_tables2/bootstrap.html"
        fields = ("name", "network", "genre", "language", "status", "premiere", "insonarr", "ignored" )