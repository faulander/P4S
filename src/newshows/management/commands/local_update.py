import os
import logging
from time import sleep
from django.core.management.base import BaseCommand, CommandError
from django.db import connection
from newshows.tasks import updateSingleShow
from newshows.models import Show, ShowType, Genre, Status, Language, Country, Network, Webchannel, Profile, Setting
import requests
import pendulum

logger = logging.getLogger("p4s")

class Command(BaseCommand):
    help = 'Update local db'
    def handle(self, *args, **options):
        site_settings = Setting.load()
        url = "https://api.tvmaze.com/updates/shows"
        db_last_update = pendulum.parse(str(site_settings.last_tvmaze_full_update), strict=False)
        logger.info(f"Last full show update: {db_last_update}")
        if pendulum.today() > db_last_update:
            while True:
                try:
                    r = requests.get(url)
                    if r.status_code == 200:
                        break
                    else:
                        logger.error("Connection to TVMaze failed.")
                except requests.exceptions.ConnectionError:
                    logger.error(f"Connection to TV Maze failed.")
                    sleep(1)
            if r.status_code == 200:
                u = r.json()
                for i in range(len(u)):
                    # updateSingleShow(str(i + 1))
                    try:
                        date_tvmaze_update = pendulum.from_timestamp(u[str(i + 1)])
                        if date_tvmaze_update >= db_last_update:
                            updateSingleShow(str(i + 1))
                    except KeyError:
                        pass
            site_settings.last_tvmaze_full_update = pendulum.now()
            site_settings.save()
