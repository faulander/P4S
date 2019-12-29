from django.db import models


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
    name = models.CharField(max_length=30)
    type = models.ForeignKey(ShowType, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, null=True, default=None)
    genre = models.ManyToManyField("Genre", related_name="shows")
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    runtime = models.IntegerField(default=0)
    premiere = models.DateTimeField(blank=True, null=True, default=None)
    network = models.ForeignKey(Network, on_delete=models.CASCADE, blank=True, null=True, default=None)
    webchannel = models.ForeignKey(Webchannel, on_delete=models.CASCADE, blank=True, null=True, default=None)
    tvrage_id = models.CharField(max_length=10, blank=True, null=True, default=None)
    thetvdb_id = models.CharField(max_length=10, blank=True, null=True, default=None)
    imdb_id = models.CharField(max_length=10, blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Shows"


class Settings(models.Model):
    setting = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __str__(self):
        return self.page.__str__()

    class Meta:
        verbose_name_plural = "Settings"
