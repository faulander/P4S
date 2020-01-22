# P4S
> Premieres for Sonarr - a small sonarr companion app to find all the new shows you've never been interested in!


P4S is a app that updates it's local database with the show information from TV Maze. You can then search for shows and conveniently adding them to Sonarr. The difference between Sonarr's own search is, that you can filter by language, premiere date, etc.

## Installation

Production:
- pull the image from docker:
```docker pull faulander/p4s:latest```
-

Development:

- make sure that you have at least Python 3.6 installed: ```python -V```
- clone or download the repository
- change into the downloaded directory
- install pipenv: ```pip install pipenv```
- install dependencies: ```pipenv install```
- run pipenv shell: ```pipenv shell```
- switch to source directory: ```cd src```
- Set Environment variables:
  - rename .env example to .env
  - fill .env with correct values (at least SONARR_API_HOST and SONARR_API_KEY need to be filled)
- run migrations: ```python manage.py migrate```
- install fixtures: ```python manage.py loaddata settings.json```
- Run the firstrun management command: ```python manage.py firstrun```

(This may run an hour, pulling 40k+ shows takes it's time. But you can open a new terminal window and start with fewer shows. It will continue to populate the db in the background)

- To Run Webserver only: ```python manage.py runserver --insecure```
- To Run Wevserver and background tasks: ```python manage.py run_huey & python manage.py runserver --insecure && fg```

## Usage
- Browse to http://localhost:8000/
- Browse to settings
- Choose at least the profile with which the shows should be added to sonarr
- Browse to shows
- Click the add button on any show you want added to Sonarr


## Release History

* 0.1.1 (current)
    * Changes to application setup for docker environment
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
