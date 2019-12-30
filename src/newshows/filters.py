from .models import Show
import django_filters


class ShowFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Show
        fields = ['name', 'network', 'language', 'genre']