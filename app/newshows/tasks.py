# Batteries first
import logging
import json
import datetime
from datetime import timedelta
import time

# Django second
from django.utils.timezone import make_aware
from django.db.models import Q
from .models import (
    Show,
    ShowType,
    Genre,
    Status,
    Language,
    Country,
    Network,
    Webchannel,
    Profile,
    Setting,
)

# 3rd party last
import requests
import pendulum

logger = logging.getLogger("p4s")

# checked for V 0.2.0
def _is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


# checked for V 0.2.0
def _requestURL(URL):
    site_settings = Setting.load()
    # logger.debug(f"Sonarr URL: {site_settings.SONARR_URL}")
    # logger.debug(f"Sonarr APIKEY: {site_settings.SONARR_APIKEY}")
    logger.debug("Trying {}".format(URL))
    headers = {"X-Api-Key": site_settings.SONARR_APIKEY}
    if site_settings.SONARR_URL and site_settings.SONARR_APIKEY:
        try:
            r = requests.get(URL, headers=headers)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            logger.error(f"Connection to {URL} raised {e}")
            return 404, False
        retValue = r.json()
        logger.debug(f"Statuscode: {r.status_code}")
        # logger.info(retValue)
        return r.status_code, retValue
    else:
        logger.error("SONARR_URL and/or SONARR_APIKEY not set")
        return 404, False


# checked for V 0.2.0
def getSonarrDownloads():
    site_settings = Setting.load()
    lstDownloads = list()
    dictShow = dict()
    endpoint = "/history"
    url = site_settings.SONARR_URL + endpoint  # + "?apikey=" + settings.SONARR_APIKEY
    statuscode, sonarr = _requestURL(url)
    if statuscode == 200:
        logger.info("History from Sonarr fetched.")
        for s in sonarr["records"]:
            # logger.info(s)
            dictShow["episode"] = s["sourceTitle"]
            dictShow["date"] = pendulum.parse(s["date"])
            lstDownloads.append(dictShow.copy())
            dictShow.clear()
        # logger.debug(lstDownloads)
        return True, lstDownloads
    else:
        logger.error("History couldn't be fetched from Sonarr.")
        return False


# checked for 0.2.0
def checkForActiveSonarr():
    """
    checks if Sonarr is reachable and updates settings
    """
    site_settings = Setting.load()
    endpoint = "/system/status"
    url = site_settings.SONARR_URL + endpoint  # + "?apikey=" + settings.SONARR_APIKEY
    statuscode, sonarr = _requestURL(url)
    if statuscode == 200:
        logger.info("Connection to Sonarr established.")
        site_settings.SONARR_OK = True
    else:
        logger.error("Connection to Sonarr failed.")
        site_settings.SONARR_OK = False
    # logger.debug(f"Settings: {site_settings}")
    site_settings.save()


# checked for 0.2.0
def HelperUpdateSonarr():
    """
    Gets the complete list of shows in Sonarr API
    If a show is found, the column 'insonarr' is set to true
    """
    site_settings = Setting.load()
    if site_settings.SONARR_OK:
        endpoint = "/series"
        url = (
            site_settings.SONARR_URL + endpoint
        )  # + "?apikey=" + settings.SONARR_APIKEY
        statuscode, sonarr = _requestURL(url)
        # logger.debug(sonarr)
        for s in sonarr:
            try:
                s_imdb = s["imdbId"]
            except KeyError:
                s_imdb = ""
            try:
                s_thetvdb = s["tvdbId"]
            except KeyError:
                s_thetvdb = ""
            try:
                s_tvmaze = s["tvMazeId"]
            except KeyError:
                s_tvmaze = ""
            try:
                s_tvrage = s["tvRageId"]
            except KeyError:
                s_tvrage = ""

            q = Show.objects.filter(
                Q(tvmaze_id=s_tvmaze)
                | Q(tvrage_id=s_tvrage)
                | Q(thetvdb_id=s_thetvdb)
                | Q(imdb_id=s_imdb)
            ).update(insonarr=True)


# checked for 0.2.0
def HelperUpdateTVMaze():
    """
    TVMazes update API provides tv shows in paged manner,
    every page contains 250 shows, leaving spaces if shows are deleted.
    the updateTvMaze function catches up from last run and gets the new shows.
    """
    while True:
        site_settings = Setting.load()
        url = "http://api.tvmaze.com/shows?page=" + str(site_settings.page)
        statuscode, shows = _requestURL(url)
        # if statuscode == 404:
        #     #ChangeSchedulingToOneDay()
        #     site_settings.page -= 1
        #     url = "http://api.tvmaze.com/shows?page=" + str(site_settings.page)
        #     statuscode, shows = _requestURL(url)
        lstGenres = list()
        for show in shows:
            if show["language"] is not None:
                dbLanguage, _ = Language.objects.get_or_create(
                    language=show["language"]
                )
            else:
                dbLanguage = None
            for genre in show["genres"]:
                try:
                    dbGenre, _ = Genre.objects.get_or_create(genre=genre)
                except Genre.MultipleObjectsReturned:
                    dbGenre = Genre.objects.filter(genre=genre).order_by("id").first()
                lstGenres.append(dbGenre)
            if show["type"] is not None:
                dbType, _ = ShowType.objects.get_or_create(type=show["type"])
            else:
                dbType = None
            dbStatus, _ = Status.objects.get_or_create(status=show["status"])
            if show["network"] is not None:
                dbCountry, _ = Country.objects.get_or_create(
                    country=show["network"]["country"]["name"],
                    code=show["network"]["country"]["code"],
                    timezone=show["network"]["country"]["timezone"],
                )
                dbNetwork, _ = Network.objects.get_or_create(
                    tvmaze_id=show["network"]["id"],
                    network=show["network"]["name"],
                    country=dbCountry,
                )
            else:
                dbNetwork = None
            if show["webChannel"] is not None:
                if show["webChannel"]["country"] is not None:
                    dbCountry, _ = Country.objects.get_or_create(
                        country=show["webChannel"]["country"]["name"],
                        code=show["webChannel"]["country"]["code"],
                        timezone=show["webChannel"]["country"]["timezone"],
                    )
                else:
                    dbCountry = None
                dbWebchannel, _ = Webchannel.objects.get_or_create(
                    tvmaze_id=show["webChannel"]["id"],
                    name=show["webChannel"]["name"],
                    country=dbCountry,
                )
            else:
                dbWebchannel = None
            if show["runtime"] is not None:
                runtime = int(show["runtime"])
            else:
                runtime = 0
            if show["premiered"] is not None:
                premiere_obj = datetime.datetime.strptime(show["premiered"], "%Y-%m-%d")
                premiere = make_aware(premiere_obj)  # make timestamp timezone aware
            else:
                premiere = None
            dbShow, created = Show.objects.get_or_create(
                tvmaze_id=show["id"],
                defaults={
                    "url": show["url"],
                    "name": show["name"],
                    "type": dbType,
                    "language": dbLanguage,
                    "status": dbStatus,
                    "runtime": runtime,
                    "premiere": premiere,
                    "network": dbNetwork,
                    "webchannel": dbWebchannel,
                    "tvrage_id": show["externals"]["tvrage"],
                    "thetvdb_id": show["externals"]["thetvdb"],
                    "imdb_id": show["externals"]["imdb"],
                },
            )
            if created:
                logger.info("New show added: {}".format(show["name"]))
            for lstGenre in lstGenres:
                lstGenre.shows.add(dbShow)
            dbShow.save()
            lstGenres.clear()
        if (
            statuscode != 429
        ):  # if we have queried the api too often, don't move on to the next page
            site_settings.page += 1
            site_settings.save()
        if statuscode == 404:  # if we reached the last page
            break
            # logger.info("Trying page {}".format(site_settings.page))


# checked for 0.2.0
def updateSingleShow(tvmaze_id):
    lstGenres = list()
    tvmaze_url = "http://api.tvmaze.com/shows/" + str(tvmaze_id)
    logger.debug(f"Trying {tvmaze_url}")
    r = requests.get(tvmaze_url)
    if r.status_code == 200:
        show = r.json()
        if show["language"] is not None:
            dbLanguage, _ = Language.objects.get_or_create(language=show["language"])
        else:
            dbLanguage = None
        for genre in show["genres"]:
            dbGenre, _ = Genre.objects.get_or_create(genre=genre)
            lstGenres.append(dbGenre)
        if show["type"] is not None:
            dbType, _ = ShowType.objects.get_or_create(type=show["type"])
        else:
            dbType = None
        dbStatus, _ = Status.objects.get_or_create(status=show["status"])
        if show["network"] is not None:
            dbCountry, _ = Country.objects.get_or_create(
                country=show["network"]["country"]["name"],
                code=show["network"]["country"]["code"],
                timezone=show["network"]["country"]["timezone"],
            )
            dbNetwork, _ = Network.objects.get_or_create(
                tvmaze_id=show["network"]["id"],
                network=show["network"]["name"],
                country=dbCountry,
            )
        else:
            dbNetwork = None
        if show["webChannel"] is not None:
            if show["webChannel"]["country"] is not None:
                dbCountry, _ = Country.objects.get_or_create(
                    country=show["webChannel"]["country"]["name"],
                    code=show["webChannel"]["country"]["code"],
                    timezone=show["webChannel"]["country"]["timezone"],
                )
            else:
                dbCountry = None
            dbWebchannel, _ = Webchannel.objects.get_or_create(
                tvmaze_id=show["webChannel"]["id"],
                name=show["webChannel"]["name"],
                country=dbCountry,
            )
        else:
            dbWebchannel = None
        if show["runtime"] is not None:
            runtime = int(show["runtime"])
        else:
            runtime = 0
        if show["premiered"] is not None:
            premiere_obj = datetime.datetime.strptime(show["premiered"], "%Y-%m-%d")
            premiere = make_aware(premiere_obj)  # make timestamp timezone aware
        else:
            premiere = None
        dbShow, updated = Show.objects.update_or_create(
            tvmaze_id=show["id"],
            defaults={
                "url": show["url"],
                "name": show["name"],
                "type": dbType,
                "language": dbLanguage,
                "status": dbStatus,
                "runtime": runtime,
                "premiere": premiere,
                "network": dbNetwork,
                "webchannel": dbWebchannel,
                "tvrage_id": show["externals"]["tvrage"],
                "thetvdb_id": show["externals"]["thetvdb"],
                "imdb_id": show["externals"]["imdb"],
            },
        )


# checked for 0.2.0
def HelperUpdateShows():
    site_settings = Setting.load()
    url = "http://api.tvmaze.com/updates/shows"
    db_last_update = pendulum.parse(
        str(site_settings.last_tvmaze_full_update), strict=False
    )
    if pendulum.today() > db_last_update:
        r = requests.get(url)
        if r.status_code == 200:
            u = r.json()
            for i in range(len(u)):
                # updateSingleShow(str(i + 1))
                try:
                    date_tvmaze_update = pendulum.from_timestamp(u[str(i + 1)])
                    if date_tvmaze_update >= db_last_update:
                        updateSingleShow(str(i + 1))
                except:
                    pass
        site_settings.last_tvmaze_full_update = pendulum.now()
        site_settings.save()


# checked for 0.2.0
# Is it really necessary to check all 5 Minutes?
# TODO: V0.3.0: Only get new profiles, if settings page is opened
def helperGetSonarrProfiles():
    site_settings = Setting.load()
    endpoint = "/profile/"
    url = site_settings.SONARR_URL + endpoint  # + "?apikey=" + settings.SONARR_APIKEY
    statuscode, sonarr = _requestURL(url)
    if statuscode == 200:
        for s in sonarr:
            dbProfile, _ = Profile.objects.get_or_create(
                profile=s["name"], profile_id=s["id"]
            )
