
# RDAutomation 🤖

This application allows automatic downloading and importing of movies (soon), TV shows, and anime into a media library (Plex, Jellyfin, Kodi). It utilizes the Real Debrid API and Torrents magnet links. The primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex or Jellyfin.


## Informations

What you need :

- A premium Real Debrid account and your API token which you can get here : https://real-debrid.com/apitoken

- Python 3

The first time you will use the app, it will ask for you API token and the location of your Plex library or media folder.
It will store those informations in the same folder as the script (plex_path, api.key and fernet.key), you API key is encrypted by fernet.key.
