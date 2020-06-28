from .models import Show
import django_filters
from django.conf import settings

class ShowFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    premiere = django_filters.DateFilter('premiere', label="premiered later than", lookup_expr='gt')

    class Meta:
        model = Show
        fields = ['name', 'network', 'webchannel', 'language', 'genre', 'premiere', 'imdb_id', 'status', 'insonarr']

    def __init__(self, *args, **kwargs):
        super(ShowFilter, self).__init__(*args, **kwargs)
        self.filters['insonarr'].label = "Show added to Sonarr?"

# checked for V 0.2.0