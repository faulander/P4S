from django.db import models
from django.contrib import messages
from django.core.cache import cache


import requests
import logging
import json

logger = logging.getLogger(__name__)

class SingletonModel(models.Model):
    """
    Abstract Class for a Singleton Model
    It only allows one row in the db and the delete method is disabled.
    To load the site settings use:
    
    from .models import Settings
    settings = Settings.load()
    
    """
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

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
    insonarr = models.BooleanField(default=False, verbose_name="S")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Shows"


class Profile(models.Model):
    profile = models.CharField(max_length=20, blank=True, null=True, default=None)
    profile_id = models.IntegerField()

    def __str__(self):
        return self.profile.__str__()

    class Meta:
        verbose_name_plural = "Profiles"


class Setting(SingletonModel):
    page = models.IntegerField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, default=None)
    addmonitored = models.BooleanField(default=True, verbose_name="Add shows as monitored to Sonnar")
    seasonfolders = models.BooleanField(default=True, verbose_name="Subfolders for seasons")
    SONARR_URL = models.CharField(max_length=1000,blank=True, verbose_name="Sonarr URL")
    SONARR_APIKEY = models.CharField(max_length=40,blank=True, verbose_name="Sonarr API-Key")
    SONARR_OK = models.BooleanField(default=False)
    SONARR_ROOTFOLDER = models.CharField(max_length=1000,blank=True, verbose_name="Sonarr Rootfolder")
    def __str__(self):
        return "Settings"

    class Meta:
        verbose_name_plural = "Settings"

