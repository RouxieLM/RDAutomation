import requests
import os
import urllib.parse
from urllib.parse import urlparse
import subprocess

def download(rd_api, magnet, show_path):
    url = "https://api.real-debrid.com/rest/1.0"
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
        subprocess.run(['curl','-#','-o', os.path.join(show_path, filename), dl_links[i]])
        print(f'Downloaded {filename} successfully.')
    
    while True:
        user_input = input("Press any key to exit.")
        if user_input == "":
            exit(0)