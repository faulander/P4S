from .models import Show, ShowType, Genre, Status, Language, Country, Network, Webchannel, Settings
import requests
from loguru import logger
from django.utils.timezone import make_aware
import datetime
from django.db.models import Q


def HelperUpdateSonarr():
    """
    Gets the complete list of shows in Sonarr API
    If a show is found, the column 'insonarr' is set to true
    """
    try:
        sonarr_url = Settings.objects.values_list('value', flat=True).get(setting="sonarr_url")  
        sonarr_apikey = Settings.objects.values_list('value', flat=True).get(setting="sonarr_apikey")
    except:
        return False
    endpoint = "/series"
    url = sonarr_url + endpoint + "?apikey=" + sonarr_apikey
    logger.debug("Trying {}", url)
    r = requests.get(url)
    statuscode = r.status_code
    logger.debug("Statuscode: {}", statuscode)
    sonarr = r.json()
    # logger.debug(sonarr)
    for s in sonarr:
        try:
            s_imdb = s['imdbId']
        except KeyError:
            s_imdb = ""
        try:
            s_thetvdb = s['tvdbId']
        except KeyError:
            s_thetvdb = ""
        try:
            s_tvmaze = s['tvMazeId']
        except KeyError:
            s_tvmaze = ""
        try:
            s_tvrage = s['tvRageId']
        except KeyError:
            s_tvrage = ""

        q = Show.objects.filter(
            Q(tvmaze_id=s_tvmaze) |
            Q(tvrage_id=s_tvrage) |
            Q(thetvdb_id=s_thetvdb) |
            Q(imdb_id=s_imdb)
        ).update(insonarr=True)


def HelperUpdateTVMaze():
    """
    TVMazes update API provides tv shows in paged manner,
    every page contains 250 shows, leaving spaces if shows are deleted.
    the updateTvMaze function catches up from last run and gets the new shows.      
    """
    try: 
        page = Settings.objects.values_list('value', flat=True).get(setting="page")  # last page which didn't result in a 404
        page = int(page)
    except:
        page = 1
    statuscode = 200
    # print(page)
    while statuscode == 200:  # as long as results are delivered 
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
                premiere = make_aware(premiere_obj)  # make timestamp timezone aware
            else:
                premiere = None
            dbShow, created = Show.objects.get_or_create(
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
            if created:
                logger.info("New show added: {}", show['name'])
            for lstGenre in lstGenres:
                lstGenre.shows.add(dbShow)
            dbShow.save()
            lstGenres.clear()
        page += 1
        Settings.objects.filter(pk=1).update(value=str(page))
    page -= 1
    Settings.objects.filter(pk=1).update(value=str(page))  # get back to last unfinished page
