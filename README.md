# P4S
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
> Premieres for Sonarr - a small sonarr companion app to find all the new shows you've never been interested in!


P4S is a app that updates it's local database with the show information from TV Maze. You can then search for shows and conveniently adding them to Sonarr. The difference between Sonarr's own search is, that you can filter by language, premiere date, etc.

## CI
![Django CI](https://github.com/faulander/P4S/workflows/Django%20CI/badge.svg?branch=master)

## Installation

Production/Docker:
- Clone the repository: ```https://github.com/faulander/P4S.git```
- change into src directory
- rename env.prod.db.example to env.prod.db and adjust the settings
- rename env.prod.example to env.prod and adjust the settings
- set firststart.prod.sh and startapp.prod.sh to executable (chmod +x)
- run ./firststart.prod.sh
- run ./startapp.prod.sh


## Usage
- Browse to http://localhost:8000/
- Browse to settings
- add Sonarr url in form of "http://localhost:8989/api"
- add the Sonarr apikey
- save
- Browse to settings
- Choose at least the profile with which the shows should be added to sonarr
- Browse to shows
- Click the add button on any show you want added to Sonarr


## Release History
* 0.4.0 First Production version with docker
* 0.3.0 (Development)
    * Docker ready
    * Switched to Whitenoise for staticfile serving
    * Switched to DjangoQ for background tasks
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

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/arogl"><img src="https://avatars1.githubusercontent.com/u/1115472?v=4" width="100px;" alt=""/><br /><sub><b>arogl</b></sub></a><br /><a href="https://github.com/faulander/P4S/commits?author=arogl" title="Tests">⚠️</a> <a href="https://github.com/faulander/P4S/commits?author=arogl" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
