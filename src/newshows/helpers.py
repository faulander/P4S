from .models import Show, ShowType, Genre, Status, Language, Country, Network, Webchannel, Settings
import requests
from loguru import logger
from django.conf import settings
from django.utils.timezone import make_aware
import datetime

def updateTvMaze():
    page = Settings.objects.values_list('value', flat=True).get(setting="page")
    page = int(page)
    statuscode = 200
    # print(page)
    while statuscode == 200:
        url = "http://api.tvmaze.com/shows?page=" + str(page)
        logger.debug("Trying {}", url)
        r = requests.get(url)
        statuscode = r.status_code
        logger.debug("Statuscode: {}", statuscode)
        shows = r.json()
        lstGenres = list()
        for show in shows:
            # logger.debug(show)
            if show['language'] is not None:
                dbLanguage, _ = Language.objects.get_or_create(language=show['language'])
            else:
                dbLanguage = None
            for genre in show["genres"]:
                dbGenre, _ = Genre.objects.get_or_create(genre=genre)
                lstGenres.append(dbGenre)
            dbType, _ = ShowType.objects.get_or_create(type=show['type'])
            dbStatus, _ = Status.objects.get_or_create(status=show['status'])
            
            if show['network'] is not None:
                dbCountry, _ = Country.objects.get_or_create(
                    country=show['network']['country']['name'],
                    code=show['network']['country']['code'],
                    timezone=show['network']['country']['timezone']
                )
                dbNetwork, _ = Network.objects.get_or_create(
                    tvmaze_id=show['network']['id'],
                    network=show['network']['name'],
                    country=dbCountry
                )
            else:
                dbNetwork = None
            if show['webChannel'] is not None:
                if show['webChannel']['country'] is not None:
                    dbCountry, _ = Country.objects.get_or_create(
                        country=show['webChannel']['country']['name'],
                        code=show['webChannel']['country']['code'],
                        timezone=show['webChannel']['country']['timezone']
                    )
                else:
                    dbCountry = None
                dbWebchannel, _ = Webchannel.objects.get_or_create(
                    tvmaze_id=show['webChannel']['id'],
                    name=show['webChannel']['name'],
                    country=dbCountry
                )
            else:
                dbWebchannel = None
            if show['runtime'] is not None:
                runtime = int(show['runtime'])
            else:
                runtime = 0
            if show['premiered'] is not None:
                premiere_obj = datetime.datetime.strptime(show['premiered'], '%Y-%m-%d')
                premiere = make_aware(premiere_obj)
            else:
                premiere = None
            dbShow, _ = Show.objects.get_or_create(
                tvmaze_id=show['id'],
                url=show['url'],
                name=show['name'],
                type=dbType,
                language=dbLanguage,
                # genre = models.ManyToManyField(Genre)
                status=dbStatus,
                runtime=runtime,
                premiere=premiere,
                network=dbNetwork,
                webchannel=dbWebchannel,
                tvrage_id=show['externals']['tvrage'],
                thetvdb_id=show['externals']['thetvdb'],
                imdb_id=show['externals']['imdb']
            )
            for lstGenre in lstGenres:
                lstGenre.shows.add(dbShow)
            dbShow.save()
            lstGenres.clear()
        page += 1
        Settings.objects.filter(pk=1).update(value=str(page))
