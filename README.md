 # P4S
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-1-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
> Premieres for Sonarr - a small sonarr companion app to find all the new shows you've never been interested in!

![P4S - Premieres for Sonarr](/screenshots/p4s.png?raw=true "P4S Main Screen")

P4S is a app that updates it's local database with the show information from TV Maze. You can then search for shows and conveniently adding them to Sonarr. The difference between Sonarr's own search is, that you can filter by language, premiere date, etc.

## CI
![Django CI](https://github.com/faulander/P4S/workflows/Django%20CI/badge.svg?branch=master)

## Installation

Production/Docker:
- Clone the repository: ```git clone https://github.com/faulander/P4S.git```
- Change into app directory ```cd P4S/app```
- Copy the example file ```cp .env.prod.example .env.prod```
- Copy the example file ```cp .env.prod.db.example .env.prod.db```
- Edit the files and enter your desired variable values
- Make the Shell files executables ```chmod +x *.sh```
- Run ```./firstart.prod.sh```
- Run ```./startapp.prod.sh```

## Usage
- Browse to http://localhost:1337/
- Browse to settings
- add Sonarr url in form of "http://ip of sonarr:8989/api"
- add the Sonarr apikey
- save
- Browse to settings
- Choose at least the profile with which the shows should be added to sonarr (if no profile is selectable, the Sonarr credentials are wrong!)
- Browse to shows
- Click the add button on any show you want added to Sonarr

## First Update of the db
If you want to update the db right away (it's afterwards scheduled), do the following:
- Browse to http://localhost:1337/admin (or wherever you installed P4S)
- Login with admin:admin
- Browse to Django Apscheduler / Django Jobs
- Run the 2 jobs: "updateTVMaze" and "updateShows" manually (you can check their progress under Django job executions)

## Meta

Harald Fauland – [@Faulander](https://twitter.com/faulander) – harald.fauland@gmail.com
Distributed under the MIT license. See ``LICENSE`` for more information.


## Contributing

1. Fork it (<https://github.com/faulander/P4S/fork>)
2. Create your feature branch (`git checkout -b yourfeaturename`)
3. Commit your changes (`git commit -am 'Add some yourfeaturename'`)
4. Push to the branch (`git push origin yourfeaturename`)
5. Create a new Pull Request

## Changes
- Dropped support for MySQL and Nginx - because it's not needed
- Changed the way the updates work

.## Contributors ✨

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
