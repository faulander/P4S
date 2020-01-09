from django.contrib import admin
from .models import Show, ShowType, Genre, Status, Language, Country, Network, Setting

admin.site.register(Show)
admin.site.register(ShowType)
admin.site.register(Genre)
admin.site.register(Status)
admin.site.register(Language)
admin.site.register(Country)
admin.site.register(Network)
admin.site.register(Setting)
