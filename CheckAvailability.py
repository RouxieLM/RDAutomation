import requests
import json

RD_API = 'key'
url = "https://api.real-debrid.com/rest/1.0"
# magnet = input('Magnet : ')
header = {"Authorization": f"Bearer {RD_API}"}
instantAvailability = "/torrents/instantAvailability/"
thash = input('hash : ')

ia = requests.get(url+instantAvailability+thash, headers=header)

json_ia = json.loads(ia.text)

if len(json_ia[f'{thash}'.lower()]) == 0:
    print('The torrent file is not available on Real Debrid, this application is not able (yet) to wait for Real Debrid to convert the magnet to a torrent file. Please add it manually via the web interface and try again. Note that it is a rare occurence, RD has thousands of torrents cached.')
    exit(0)
else:
    print('Torrent available on Real Debrid, proceeding to download.')