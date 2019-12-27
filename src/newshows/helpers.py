from .models import Show, ShowType, Genre, Status, Language, Country, Network, Settings
import requests

def updateTvMaze():
    try:
        page = Settings.objects.values_list('page', flat=True).get(pk=1)
    except:
        page = 1
    statuscode = 200
    # print(page)
    while statuscode == 200:
        url = "http://api.tvmaze.com/shows?page=" + str(page)
        r = requests.get(url)
        statuscode = r.status_code
        shows = r.json()
        for show in shows:
            dbLanguage, _ = Language.objects.get_or_create(language=show['language'])
            for genre in show["genres"]:
                dbGenre, _ = Genre.objects.get_or_create(genre=genre)
            dbType, _ = ShowType.objects.get_or_create(type=show['type'])
            dbCountry, _ = Country.objects.get_or_create(
                country=show['network']['country']['name'],
                code=show['network']['country']['code'],
                timezone=show['network']['country']['timezone']
            )
            dbStatus,_ = Status.objects.get_or_create(status=show['status'])
            dbNetwork, _ = Network.objects.get_or_create(
                tvmaze_id=show['network']['id'],
                network=show['network']['name'],
                country=dbCountry
            )
            dbShow, _ = Show.objects.get_or_create(
                tvmaze_id=show['id'],
                url=show['url'],
                name=show['name'],
                type=dbType,
                language=dbLanguage,
                # genre = models.ManyToManyField(Genre)
                status=dbStatus,
                runtime=str(show['runtime']),
                premiere=show['premiered'],
                network=dbNetwork,
                tvrage_id=show['externals']['tvrage'],
                thetvdb_id=show['externals']['thetvdb'],
                imdb_id=show['externals']['imdb']
            )
            page += 1
    Settings.objects.filter(pk=1).update(page=page)


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