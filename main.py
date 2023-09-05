import os
import requests
import shutil
import json
import re
from cryptography.fernet import Fernet
import urllib.parse
from urllib.parse import urlparse
from pick import pick


print("\nThis application enables automatic downloading and importing of movies, TV shows, and anime into a Plex media library. It utilizes the Real Debrid API and Torrents magnet links. The primary objective of this project is to facilitate the swift and automated importation of entire seasons of TV shows or anime into Plex.\n\nIf you want to reset your settings, simply delete all the files except for main.py.\n\n")
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

qurl = "https://apibay.org/q.php?q="
furl = "https://apibay.org/f.php?id="

show_name = input('[Mandatory] Name of the show : ')
season = input('[Optionnal] Season (only the number) : ')

if season:
    query = requests.get(qurl+show_name+' season '+season)
    query_json = json.loads(query.text)
    pattern = rf'season {season}'.lower()
    query_json = [item for item in query_json if re.search(pattern, item['name'].lower())]
else:
    query = requests.get(qurl+show_name)
    query_json = json.loads(query.text)

filtered_list = []

for item in query_json:
    if item['status'] == 'VIP'.lower():
        item['status'] = '[SAFE] Posted by VIP member'
    elif item['status'] == 'Trusted'.lower():
        item['status'] = '[SAFE] Posted by trusted member'
    else:
        item['status'] = '[UNSAFE] Posted by untrusted account'

    bytes_size = int(item['size'])
    gigabyte_size = bytes_size / (1024 * 1024 * 1024)

    formatted_size = "{:.2f}".format(gigabyte_size)
    item['size'] = formatted_size + " GB"

    item_dict = {
        'id': item['id'],
        'name': item['name'],
        'size': item['size'],
        'info_hash': item['info_hash'],
        'status': item['status']
    }

    filtered_list.append(item_dict)

max_name_len = max(len(item['name']) for item in query_json)
max_size_len = max(len(item['size']) for item in query_json)
max_status_len = max(len(item['status']) for item in query_json)
max_id_len = max(len(item['id']) for item in query_json)

display_items = []
for item in query_json:
    formatted_item = f"{item['name']:{max_name_len}} | {item['size']:{max_size_len}} | {item['status']:{max_status_len}} | ID: {item['id']:{max_id_len}}"
    display_items.append(formatted_item)

title = "Choose a torrent:"
selected_item, selected_index = pick(display_items, title, indicator='->')

id_match = re.search(r'ID:\s*(\d+)', selected_item)
selected_id = id_match.group(1)

for item in query_json:
    if item['id'] == selected_id:
        selected_thash = item['info_hash']
        selected_name = item['name']

print(selected_thash)
print(selected_name)

encoded_dn = urllib.parse.quote(selected_name)

print(encoded_dn)

magnet = f"magnet:?xt=urn:btih:{selected_thash}&dn={encoded_dn}&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.bittor.pw%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Fbt.xxx-tracker.com%3A2710%2Fannounce&tr=udp%3A%2F%2Fpublic.popcorn-tracker.org%3A6969%2Fannounce&tr=udp%3A%2F%2Feddie4.nl%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"

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