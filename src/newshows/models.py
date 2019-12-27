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

# Create your models here.
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


""" 
	"id":250,
	"url":"http://www.tvmaze.com/shows/250/kirby-buckets",
	"name":"Kirby Buckets",
	"type":"Scripted",
	"language":"English",
	"genres":
		["Comedy"],
	"status":"Ended",
	"runtime":30,
	"premiered":"2014-10-20",
	"officialSite":"http://disneyxd.disney.com/kirby-buckets",
	"schedule":{
		"time":"07:00",
		"days":
			["Monday","Tuesday","Wednesday","Thursday","Friday"]
		},
	"rating":{
		"average":null
		},
	"weight":0,
	"network":{
		"id":25,
		"name":"Disney XD",
		"country":{
			"name":"United States",
			"code":"US",
			"timezone":"America/New_York"
			}
		},
	"webChannel":{
		"id":83,
		"name":"DisneyNOW",
		"country":{
			"name":"United States",
			"code":"US",
			"timezone":"America/New_York"
		}
	},
	"externals":{
		"tvrage":37394,
		"thetvdb":278449,
		"imdb":"tt3544772"
		},
	"image":{
		"medium":"http://static.tvmaze.com/uploads/images/medium_portrait/1/4600.jpg",
		"original":"http://static.tvmaze.com/uploads/images/original_untouched/1/4600.jpg"
        },
    "summary":"<p>The single-camera series that mixes live-action and animation stars Jacob Bertrand as the title character. <b>Kirby Buckets</b> introduces viewers to the vivid imagination of charismatic 13-year-old Kirby Buckets, who dreams of becoming a famous animator like his idol, Mac MacCallister. With his two best friends, Fish and Eli, by his side, Kirby navigates his eccentric town of Forest Hills where the trio usually find themselves trying to get out of a predicament before Kirby's sister, Dawn, and her best friend, Belinda, catch them. Along the way, Kirby is joined by his animated characters, each with their own vibrant personality that only he and viewers can see.</p>",
	"updated":1574820377,
	"_links":{
		"self":{"href":"http://api.tvmaze.com/shows/250"},
		"previousepisode":{"href":"http://api.tvmaze.com/episodes/1051658"}
	}
} """