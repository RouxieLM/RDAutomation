import requests
import shutil
import os
import urllib.parse
from urllib.parse import urlparse
import json
import subprocess

url = "https://api.real-debrid.com/rest/1.0"

def check_availability(rd_api, selected_thash):
    header = {"Authorization": f"Bearer {rd_api}"}
    instantAvailability = "/torrents/instantAvailability/"

    ia = requests.get(url+instantAvailability+selected_thash, headers=header)

    json_ia = json.loads(ia.text)

    if len(json_ia[f'{selected_thash}'.lower()]) == 0:
        print('The torrent file is not available on Real Debrid, this application is not able (yet) to wait for Real Debrid to convert the magnet to a torrent file and download its content. Please add it manually via the web interface and try again. Note that it is a rare occurence, RD has thousands of torrents cached.')
        exit(0)
    else:
        print('Torrent available on Real Debrid, proceeding to download...')


def download(rd_api, magnet, season_path):
    header = {"Authorization": f"Bearer {rd_api}"}
    torrents = "/torrents"
    unrestrict = "/unrestrict/link"
    addMagnet = "/torrents/addMagnet"
    data_magnet = {"magnet": magnet}
    selectFiles = "/torrents/selectFiles/"
    data_select_files = {"files" : "all"}

    post_magnet = requests.post(url+addMagnet, headers=header, data=data_magnet)
    post_magnet_json = post_magnet.json()
    tid = post_magnet_json['id']

    requests.post(url+selectFiles+tid, headers=header, data=data_select_files)

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
        filename = urllib.parse.unquote(os.path.basename(parsed_url.path))
        print(f'\nDownloading {filename}...')
        subprocess.run(['curl','-#','-o', os.path.join(season_path, filename), dl_links[i]])
        print(f'Downloaded {filename} successfully.')