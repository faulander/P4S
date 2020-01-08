from django.db import models
from django.contrib import messages

import requests
import logging
import json

logger = logging.getLogger(__name__)


class ShowType(models.Model):
    type = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = "Show Types"


class Language(models.Model):
    language = models.CharField(max_length=30)

    def __str__(self):
        return self.language

    class Meta:
        verbose_name_plural = "Languages"


class Genre(models.Model):
    genre = models.CharField(max_length=30)

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name_plural = "Genres"



class Status(models.Model):
    status = models.CharField(max_length=30)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name_plural = "Status"


class Country(models.Model):
    country = models.CharField(max_length=30)
    code = models.CharField(max_length=10)
    timezone = models.CharField(max_length=30)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name_plural = "Countries"


class Network(models.Model):
    tvmaze_id = models.IntegerField()
    network = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.network

    class Meta:
        verbose_name_plural = "Networks"


class Webchannel(models.Model):
    tvmaze_id = models.IntegerField()
    name = models.CharField(max_length=30)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Webchannels"


class Show(models.Model):
    tvmaze_id = models.IntegerField()
    url = models.CharField(max_length=100, blank=True, null=True, default=None)
    name = models.CharField(max_length=30, verbose_name="Show")
    type = models.ForeignKey(ShowType, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, null=True, default=None)
    genre = models.ManyToManyField("Genre", related_name="shows")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    runtime = models.IntegerField(default=0)
    premiere = models.DateTimeField(blank=True, null=True, default=None, verbose_name="premiered")
    network = models.ForeignKey(Network, on_delete=models.CASCADE, blank=True, null=True, default=None)
    webchannel = models.ForeignKey(Webchannel, on_delete=models.CASCADE, blank=True, null=True, default=None)
    tvrage_id = models.CharField(max_length=10, blank=True, null=True, default=None)
    thetvdb_id = models.CharField(max_length=10, blank=True, null=True, default=None)
    imdb_id = models.CharField(max_length=10, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ignored = models.BooleanField(default=False, verbose_name="I")
    insonarr = models.BooleanField(default=False, verbose_name="S")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Shows"


class Settings(models.Model):
    setting = models.CharField(max_length=50, blank=True, null=True, default=None)
    value = models.CharField(max_length=100, blank=True, null=True, default=None)

    def __str__(self):
        return self.setting.__str__()

    class Meta:
        verbose_name_plural = "Settings"


class Profile(models.Model):
    profile = models.CharField(max_length=20, blank=True, null=True, default=None)
    profile_id = models.IntegerField()

    def __str__(self):
        return self.profile.__str__()

    class Meta:
        verbose_name_plural = "Profiles"


class Setting(models.Model):
    page = models.IntegerField()
    sonarr_url = models.CharField(max_length=100, blank=True, null=True, default=None, verbose_name="Sonarr URL")
    sonarr_apikey = models.CharField(max_length=50, blank=True, null=True, default=None, verbose_name="Sonarr API Key")
    sonarr_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Sonarr Profile ID")
    sonarr_autoadd = models.BooleanField(default=False, verbose_name="Auto add shows to Sonarr")
    sonarr_ok = models.BooleanField(default=False, verbose_name="Settings for Sonarr ok")

    def __str__(self):
        return "Settings"

    class Meta:
        verbose_name_plural = "Settings"
    
    #  Upon saving let's try and get the status of Sonarr
    #  If the response isn't valid JSON, the details are wrong
    #  and the sonarr_ok setting is set to False
    #  If the response is valid JSON, the sonarr_ok setting is set to True
    #  Shows should show up with the correct buttons and column
    
    def save(self, *args, **kwargs):
        if self.sonarr_url and self.sonarr_apikey:
            # both url and apikey are set
            endpoint = "/system/status"
            url = self.sonarr_url + endpoint + "?apikey=" + self.sonarr_apikey
            logger.info("Trying {}".format(url))
            r = requests.get(url)
            statuscode = r.status_code
            logger.info("Statuscode: {}".format(statuscode))
            if statuscode == 200:
                try:
                    sonarr = r.json()
                except json.decoder.JSONDecodeError:
                    self.sonarr_ok = False
                    sonarr = None
                    # messages.warning("Sonarr connection failed.")
                if sonarr is not None:
                    self.sonarr_ok = True
                else:
                    self.sonarr_ok = False
            else:
                self.sonarr_ok = False
                # messages.warning(request, "Sonarr connection failed.")

        super(Setting, self).save(*args, **kwargs)
        