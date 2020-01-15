# P4S
> Premieres for Sonarr - a small sonarr companion app to find all the new shows you've never been interested in!


P4S is a app that updates it's local database with the show information from TV Maze. You can then search for shows and conveniently adding them to Sonarr. The difference between Sonarr's own search is, that you can filter by language, premiere date, etc.

## Installation

Development:

- clone or download the repository
- create a virtual environment and activate it
```python -m venv .venv```
- install dependencies with 
```pip install -r requirements.txt```
- run migrations with 
```python manage.py migrate```
- install fixtures with 
```python manage.py loaddata settings.json```
- Set Environment variables:

Windows:
```
set SONARR_URL=http://192.168.1.10:8989/
set SONARR_APIKEY=3jsehfu4853475hsdjf84
(change to the real values)
  ```
Linux:
```
export SONARR_URL="http://192.168.1.10:8989/"
export SONARR_APIKEY="3jsehfu4853475hsdjf84"
(change to the real values)
```

To Run Webserver only:
```python manage.py runserver```

To Run Wevserver and background tasks
```python manage.py run_huey & python manage.py runserver && fg```

## Usage
- Browse to http://localhost:8000/
- Browse to settings
- Choose at least the profile with which the shows should be added to sonarr
- Browse to shows
- Click the add button on any show you want added to Sonarr


## Release History

* 0.1.0
    * The first proper release

## Meta

Harald Fauland – [@Faulander](https://twitter.com/faulander) – harald.fauland@gmail.com
Distributed under the MIT license. See ``LICENSE`` for more information.


## Contributing

1. Fork it (<https://github.com/faulander/P4S/fork>)
2. Create your feature branch (`git checkout -b yourfeaturename`)
3. Commit your changes (`git commit -am 'Add some yourfeaturename'`)
4. Push to the branch (`git push origin yourfeaturename`)
5. Create a new Pull Request
