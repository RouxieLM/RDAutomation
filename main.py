import os
import requests
import shutil
from cryptography.fernet import Fernet
from urllib.parse import urlparse
from pick import pick

print("\nThis application enables automatic downloading and importing of movies, TV shows, and anime into a Plex media library. It utilizes the Real Debrid API and Torrents magnet links. The primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex.\nIf you want to reset your settings, simply delete all the files except for main.py.\n")
input("Press Enter to continue...")

if os.path.exists("fernet.key"):
    with open("fernet.key", "rb") as file :
        key = file.read()
else: 
    key = Fernet.generate_key()
    with open("fernet.key", "wb") as file :
        file.write(key)

if os.path.exists("api.key"):
    with open("api.key", "rb") as file :
        encrypted_RD_API = file.read()
else:
    print("\nIt seems that your API key is not known by the application, please provide it.\n")
    RD_API = input("RD API key: ").encode()

    with open("fernet.key", "rb") as file :
        key = file.read()
        f = Fernet(key)
    encrypted_RD_API = f.encrypt(RD_API)
    with open("api.key", "wb") as file :
        file.write(encrypted_RD_API)

f = Fernet(key)
RD_API = f.decrypt(encrypted_RD_API).decode('utf-8')

if os.path.exists("plex_path"):
    with open("plex_path", "r") as file :
        plex_path = file.read()
else:
    plex_path = input("It seems that the Plex path is not known by the application. Please provide the full Plex media library path: ")
    with open("plex_path", "w") as file :
        file.write(plex_path)

title = "Please choose the type of media you want to import: "
options = ['Films', 'Séries', 'Anime']

option, index = pick(options, title, indicator='->', default_index=0)

show_name = input(f"Please provide the name of the {option}: ")

if option == "Séries" or option == "Anime":
    season = input("Please provide which season you are importing, only type a number: ")
else:
    pass

if os.path.exists(plex_path):
    show_path = os.path.join(plex_path, option, show_name)
else:
    print("Error, plex path not found.")
    exit(1)

if not os.path.exists(show_path):
    os.makedirs(show_path)
else:
    print(f"{show_path} folder already exists.")

if option == "Séries" or option == "Anime":
    season_path = os.path.join(show_path, f'Saison {season}')

    if not os.path.exists(season_path):
        os.makedirs(season_path)
        print(f"successfully created {season_path} folder.")
    else:
        print(f'{season_path} folder already exists.')
else:
    pass

magnet = input('Please provide the torrent magnet link: ')

url = "https://api.real-debrid.com/rest/1.0"
header = {"Authorization": f"Bearer {RD_API}"}
torrents = "/torrents"
torrents_info = "/torrents/info/"
unrestrict = "/unrestrict/link"
addMagnet = "/torrents/addMagnet"
data_magnet = {"magnet": magnet}
selectFiles = "/torrents/selectFiles/"
data_select_files = {"files" : "all"}

post_magnet = requests.post(url+addMagnet, headers=header, data=data_magnet)
post_magnet_json = post_magnet.json()
tid = post_magnet_json['id']

select_files = requests.post(url+selectFiles+tid, headers=header, data=data_select_files)

torrent = requests.get(url+torrents, headers=header)
torrent_json = torrent.json()
rd_links = (torrent_json[0]['links'])
len_links = (len(rd_links))

dl_links = []

for i in range(len_links):
    link = rd_links[i]
    data = {"link" : link}
    dl_link_req = requests.post(url+unrestrict, headers=header, data=data)
    dl_link_json = dl_link_req.json()
    dl_links.append(dl_link_json['download'])

len_dl_links = len(dl_links)

for i in range(len_dl_links):
    parsed_url = urlparse(dl_links[i])
    filename = os.path.basename(parsed_url.path)
    print(f'\nDownloading {filename}...')
    response = requests.get(dl_links[i])
    with open(filename, "wb") as file :
        file.write(response.content)
    shutil.move(filename, season_path)
    print(f'Downloaded {filename} successfully.')