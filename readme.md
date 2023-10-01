# RDAutomation 🤖

This application allows automatic downloading and importing of movies, TV shows, and anime into a media library (Plex, Jellyfin...). It utilizes the Real Debrid API and torrent magnet links. The primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex or Jellyfin.


## Informations

What you need :

- A premium Real Debrid account and your API token which you can get here : https://real-debrid.com/apitoken

The first time you will use the app, it will ask for you API token and the location of your Plex library or media folder.
It will store those informations in the same folder as the script (plex_path, api.key and fernet.key), your API key is encrypted by fernet.key.



## Features

- Torrent search
- Torrent picking within the app with name, size, trust factor and ID
- Automatic magnet generation
- Automatic downloads of Movies, TV Shows and Anime
- Progress bar for downloads


## What I'm working on

- File selector (currently, the app downloads all files present in the torrent)
- Multiple torrent sites (currently, the app is scraping TPB)
- Better search filter
- WebUI / UI
- Jellyfin integration
