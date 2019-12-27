from .models import Show, ShowType, Genre, Status, Language, Country, Network, Settings


def updateTvMaze():
    page = str(Settings.objects.values_list('page', flat=True).get(pk=1))
    
    # print(page)
    url = "http://api.tvmaze.com/shows?page=" + page
    
