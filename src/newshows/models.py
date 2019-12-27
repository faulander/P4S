from django.db import models


class ShowType(models.Model):
    type = models.CharField(max_length=30)

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
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.network

    class Meta:
        verbose_name_plural = "Networks"


class Show(models.Model):
    tvmaze_id = models.IntegerField()
    url = models.CharField(max_length=100)
    name = models.CharField(max_length=30)
    type = models.ForeignKey(ShowType, on_delete=models.CASCADE)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    genre = models.ManyToManyField(Genre)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    runtime = models.IntegerField()
    premiere = models.DateTimeField()
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    tvrage_id = models.CharField(max_length=10)
    thetvdb_id = models.CharField(max_length=10)
    imdb_id = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Shows"


class Settings(models.Model):
    page = models.IntegerField()

    def __str__(self):
        return self.page.__str__()

    class Meta:
        verbose_name_plural = "Settings"
