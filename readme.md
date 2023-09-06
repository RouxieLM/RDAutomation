# RDAutomation 🤖

This application allows automatic downloading and importing of movies (soon), TV shows, and anime into a media library (Plex, Jellyfin...). It utilizes the Real Debrid API and torrent magnet links. The primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex or Jellyfin.


## Informations

What you need :

- A premium Real Debrid account and your API token which you can get here : https://real-debrid.com/apitoken

- Python 3

The first time you will use the app, it will ask for you API token and the location of your Plex library or media folder.
It will store those informations in the same folder as the script (plex_path, api.key and fernet.key), you API key is encrypted by fernet.key.



## Features

- Torrent search
- Torrent picking within the app with name, size, trust factor and ID
- Automatic magnet generation
- Automatic downloads
- Media folders management



## Upcoming

- Movies support
- Files selector (currently, the app downloads all files present in the torrent)
- Progress bar for downloads
- Multiple torrent sites (currently, the app is scraping TBP)
- Better search filter
- Better path management
- WebUI