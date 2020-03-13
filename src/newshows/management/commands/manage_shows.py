# disabled for 0.2.0
# for 0.3.0
"""
import logging
import requests

from django.core.management.base import BaseCommand, CommandError

import new_shows.settings as settings
from newshows.helpers import _is_json

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Shows or deletes shows which are available publically eg on Netflix or Amazon'

    def handle(self, *args, **kwargs):

        RAPIDAPI_POSSIBLE_COUNTRIES = ("uk", "us", "ar", "at", "au", "be", "br", "ca",
                                       "ch", "cz", "dk", "de", "ee", "es", "fr", "hk",
                                       "hu", "ie", "il", "in", "is", "it", "jp", "kr",
                                       "lt", "lv", "mx", "nl", "no", "nz", "ph", "pl",
                                       "pt", "ro", "ru", "se", "sg", "sk", "th", "za")
        RAPIDAPI_POSSIBLE_HOSTS = ("Netflix", "Amazon Prime Video", "Amazon Instant Video",
                                   "Apple TV+", "Google Play", "iTunes", "YouTube Premium",
                                   "Disney Plus", "Hulu", "Atom Tickets", "CBS", "DC Universe",
                                   "HBO", "Discovery Channel", "Fandango Movies", "Fox", "NBC",
                                   "Nickelodeon")

        for country in settings.RAPIDAPI_COUNTRIES:
            if country not in RAPIDAPI_POSSIBLE_COUNTRIES:
                raise CommandError("Country '%s' not in allowed list." % country)
        for host in settings.RAPIDAPI_HOSTS:
            if host not in RAPIDAPI_POSSIBLE_HOSTS:
                raise CommandError("Host '%s' not in allowed list." % host)

        url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"

        querystring = {"term": "Hell on Wheels", "country": "de"}

        headers = {
            'x-rapidapi-host': settings.RAPIDAPI_HOST,
            'x-rapidapi-key': settings.RAPIDAPI_KEY
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
"""