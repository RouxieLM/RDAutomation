import requests
import json
import re
from pick import pick
import urllib.parse

def scraper():
    qurl = "https://apibay.org/q.php?q="
    furl = "https://apibay.org/f.php?id="

    print('\nYou will now search for the desired content. Try to be precise for simple show names like "Dark" for example, the search function is far from perfect for now. The app will first ask you for general terms, and then the season number if needed.\n')
    scraper_show_name = input('[Mandatory] What do you want to download ? Example : Dark x264 1080p\n')
    scraper_season = input('[Optionnal] Season (only the number) : ')

    if scraper_season:
        query = requests.get(qurl+scraper_show_name+' season '+scraper_season)
        query_json = json.loads(query.text)
        pattern = rf'season {scraper_season}'.lower()
        query_json = [item for item in query_json if re.search(pattern, item['name'].lower())]
    else:
        query = requests.get(qurl+scraper_show_name)
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

    encoded_dn = urllib.parse.quote(selected_name)

    magnet = f"magnet:?xt=urn:btih:{selected_thash}&dn={encoded_dn}&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.bittor.pw%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Fbt.xxx-tracker.com%3A2710%2Fannounce&tr=udp%3A%2F%2Fpublic.popcorn-tracker.org%3A6969%2Fannounce&tr=udp%3A%2F%2Feddie4.nl%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"

    return magnet