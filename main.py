# -*- coding: utf-8 -*-

from qbittorrent import Client
from sonarr_api import SonarrAPI

# qb.login('admin', 'adminadmin') # not required when 'Bypass from localhost' setting is active.
qb = Client('http://qbittorrent.local:6880/')
qb.login()


sonarr_host_url = 'http://sonarr.local:6880/api'
sonarr_api_key = '589b093bc3484ea5b941173280df0911'


def getTorrents():
    torrents = qb.torrents()

    hash_list = []
    for torrent in torrents:
        if torrent['amount_left'] == 0:
            print(f"qBittorrent: Removing {torrent['name']}")
            hash_list.append(torrent['hash'])
        else:
            print(f"qBittorrent: Keeping {torrent['name']}")
    return hash_list


def removeTorrent(hash_list):
    qb.delete_permanently(hash_list)


def getSonarrHistory():
    # Instantiate SonarrAPI Object
    sonarr = SonarrAPI(sonarr_host_url, sonarr_api_key)

    # Get and print TV Shows
    hist = sonarr.get_history()
    for record in hist['records']:
        if record['data']['downloadClient'] == 'QBittorrent':
            print(f"Sonarr: {record['data']['downloadClient']} - {record['sourceTitle']}")

if __name__ == '__main__':
    torrents = getTorrents()
    removeTorrent(torrents)
    getSonarrHistory()
