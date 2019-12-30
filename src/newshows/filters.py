from .models import Show
import django_filters


class ShowFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    premiere = django_filters.DateFilter('premiere', label="premiered later than", lookup_expr='gt')

    class Meta:
        model = Show
        fields = ['name', 'network', 'webchannel', 'language', 'genre', 'premiere', 'imdb_id', 'status', 'insonarr', 'ignored']
    
    def __init__(self, *args, **kwargs):
       super(ShowFilter, self).__init__(*args, **kwargs)
       self.filters['insonarr'].label="Show added to Sonarr?"
       self.filters['ignored'].label="Ignored?"
       