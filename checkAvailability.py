import requests
import json

def check_availability(rd_api, selected_thash):
    url = "https://api.real-debrid.com/rest/1.0"
    header = {"Authorization": f"Bearer {rd_api}"}
    instantAvailability = "/torrents/instantAvailability/"

    ia = requests.get(url+instantAvailability+selected_thash, headers=header)

    json_ia = json.loads(ia.text)

    if len(json_ia[f'{selected_thash}'.lower()]) == 0:
        print('The torrent file is not available on Real Debrid, this application is not able (yet) to wait for Real Debrid to convert the magnet to a torrent file and download its content. Please add it manually via the web interface and try again. Note that it is a rare occurence, RD has thousands of torrents cached.')
        exit(0)
    else:
        print('Torrent available on Real Debrid, proceeding to download...')