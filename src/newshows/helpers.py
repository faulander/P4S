# Batteries first
import logging
import json
import datetime
from datetime import timedelta
# Django second
from django.utils.timezone import make_aware
from django.db.models import Q
from .models import Show, ShowType, Genre, Status, Language, Country, Network, Webchannel, Profile, Setting
# 3rd party last
import requests
import pendulum
from loguru import logger
from background_task import background

# checked for V 0.2.0
def _is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

# checked for V 0.2.0
def _requestURL(URL, METHOD="get"):
    logger.info("Trying {}".format(URL))
    try:
        r = requests.get(URL)
    except:
        return False, False
    try:
        retValue = r.json()
    except:
        return False, False
    return r.status_code, retValue

# checked for V 0.2.0
@background(schedule=60)
def getSonarrDownloads():
    settings = Setting.load()
    lstDownloads = list()
    dictShow = dict()
    endpoint = "/history/"
    url = settings.SONARR_URL + endpoint + "?apikey=" + settings.SONARR_APIKEY
    statuscode, sonarr = _requestURL(url)
    if statuscode == 200: 
        logger.info("History from Sonarr fetched.")
        for s in sonarr['records']:
            # logger.info(s)
            dictShow['episode'] = s['sourceTitle']
            dictShow['date'] = pendulum.parse(s['date'])
            lstDownloads.append(dictShow.copy())
            dictShow.clear()
        logger.info(lstDownloads)
        return True, lstDownloads
    else:
        logger.error("History couldn't be fetched from Sonarr.")
        return False

# checked for 0.2.0
@background(schedule=60)
def checkForActiveSonarr():
    """
    checks if Sonarr is reachable and updates settings 
    """
    settings = Setting.load()
    endpoint = "/system/status/"
    url = settings.SONARR_URL + endpoint + "?apikey=" + settings.SONARR_APIKEY
    statuscode, sonarr = _requestURL(url)
    if statuscode == 200:
        logger.info("Connection to Sonarr established.")
        settings.SONARR_OK = True
    else:
        logger.error("Connection to Sonarr failed.")
        settings.SONARR_OK = False
    logger.debug(f"Settings: {settings}")
    settings.save()

# checked for 0.2.0
@background(schedule=300)
def HelperUpdateSonarr():
    """
    Gets the complete list of shows in Sonarr API
    If a show is found, the column 'insonarr' is set to true
    """
    settings = Setting.load()
    if settings.SONARR_OK:
        endpoint = "/series"
        url = settings.SONARR_URL + endpoint + "?apikey=" + settings.SONARR_APIKEY
        statuscode, sonarr = _requestURL(url)
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

# checked for 0.2.0
@background(schedule=180)
def HelperUpdateTVMaze():
    """
    TVMazes update API provides tv shows in paged manner,
    every page contains 250 shows, leaving spaces if shows are deleted.
    the updateTvMaze function catches up from last run and gets the new shows.
    """
    settings = Setting.load()
    statuscode = 0
    page = settings.page
    if not page:
        page = 0
    while statuscode != 200:
        url = "http://api.tvmaze.com/shows?page=" + str(page)
        statuscode, shows = _requestURL(url)
        page -= 1
    lstGenres = list()
    for show in shows:
        if show['language'] is not None:
            dbLanguage, _ = Language.objects.get_or_create(language=show['language'])
        else:
            dbLanguage = None
        for genre in show["genres"]:
            dbGenre, _ = Genre.objects.get_or_create(genre=genre)
            lstGenres.append(dbGenre)
        if show['type'] is not None:
            dbType, _ = ShowType.objects.get_or_create(type=show['type'])
        else:
            dbType = None
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
            defaults={
                'url': show['url'],
                'name': show['name'],
                'type': dbType,
                'language': dbLanguage,
                'status': dbStatus,
                'runtime': runtime,
                'premiere': premiere,
                'network': dbNetwork,
                'webchannel': dbWebchannel,
                'tvrage_id': show['externals']['tvrage'],
                'thetvdb_id': show['externals']['thetvdb'],
                'imdb_id': show['externals']['imdb']
            }
        )
        if created:
            logger.info("New show added: {}".format(show['name']))
        else:
            logger.info("Show already in DB: {}".format(show['name']))
        for lstGenre in lstGenres:
            lstGenre.shows.add(dbShow)
        dbShow.save()
        lstGenres.clear()
    page += 1
    settings.page = page
    logger.debug(f"Settings: {settings}")
    settings.save()

#checked for 0.2.0
def updateSingleShow(tvmaze_id):
    lstGenres = list()
    url = "http://api.tvmaze.com/shows/" + str(tvmaze_id)
    r = requests.get(url)
    if r.status_code == 200:
        show = r.json()
        if show['language'] is not None:
            dbLanguage, _ = Language.objects.get_or_create(language=show['language'])
        else:
            dbLanguage = None
        for genre in show["genres"]:
            dbGenre, _ = Genre.objects.get_or_create(genre=genre)
            lstGenres.append(dbGenre)
        if show['type'] is not None:
            dbType, _ = ShowType.objects.get_or_create(type=show['type'])
        else:
            dbType = None
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
        dbShow = Show.objects.get(tvmaze_id=show['id'])
        dbShow.url = show['url']
        dbShow.name = show['name']
        dbShow.type = dbType
        dbShow.language = dbLanguage
        dbShow.status = dbStatus
        dbShow.runtime = runtime
        dbShow.premiere = premiere
        dbShow.network = dbNetwork
        dbShow.webchannel = dbWebchannel
        dbShow.tvrage_id = show['externals']['tvrage']
        dbShow.thetvdb_id = show['externals']['thetvdb']
        dbShow.imdb_id = show['externals']['imdb']
        dbShow.save()
        logger.info("Show '{}' updated.".format(show['name']))

#checked for 0.2.0
@background(schedule=10800)
def HelperUpdateShows():
    settings = Setting.load()
    url = "http://api.tvmaze.com/updates/shows"
    r = requests.get(url)
    if r.status_code == 200:
        u = r.json()
        for i in range(len(u)):
            # updateSingleShow(str(i + 1))
            try:
                d1 = pendulum.from_timestamp(u[str(i + 1)])
                d2 = pendulum.now()
                delta = d2 - d1
                if delta.days < 2:
                    #  Show has been updated in the last 2 days
                    # we are running the tvmaze update every 24 hours, so we are save
                    # to get all updates
                    updateSingleShow(str(i + 1))
            except KeyError:
                pass

#checked for 0.2.0
# Is it really necessary to check all 5 Minutes?
# TODO: Only get new profiles, if settings page is opened
@background(schedule=360))
def helperGetSonarrProfiles():
    settings = Setting.load()
    endpoint = "/profile/"
    url = settings.SONARR_URL + endpoint + "?apikey=" + settings.SONARR_APIKEY
    statuscode, sonarr = _requestURL(url)
    if statuscode == 200:
        Profile.objects.all().delete()  # First delete all current profiles
        
        for s in sonarr:
            dbProfile, _ = Profile.objects.get_or_create(
                profile=s['name'],
                profile_id=s['id']
            )