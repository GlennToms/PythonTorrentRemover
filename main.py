# -*- coding: utf-8 -*-

from qbittorrent import Client
from sonarr_api import SonarrAPI

# qb.login('admin', 'adminadmin') # not required when 'Bypass from localhost' setting is active.
qb = Client('http://qbittorrent.local:6880/')
qb.login()


sonarr_host_url = 'http://sonarr.local:6880/api'
sonarr_api_key = '589b093bc3484ea5b941173280df0911'


# def get_torrents():
#     torrents = qb.torrents()

#     torrent_list = []
#     for torrent in torrents:
#         if torrent['amount_left'] == 0:
#             print(f"qBittorrent: Removing {torrent['name']}")
#             torrent_list.append(torrent['hash'])
#         else:
#             print(f"qBittorrent: Keeping {torrent['name']}")
#     return torrent_list

def get_torrents():
    torrents = qb.torrents()

    torrent_list = []
    for torrent in torrents:
        if torrent['amount_left'] == 0:
            torrent_list.append((torrent['name'], torrent['hash']))
    return torrent_list


def remove_complete_torrents(torrent_list, sonarr_list):
    remove_list = []
    for torrent in torrent_list:
        for history in sonarr_list:
            if torrent[0] in history:
                print(f"Removing: {torrent[0]}")
                remove_list.append(torrent[1])

    #qb.delete_permanently(remove_list)

def pause_complete():
    torrents = get_torrents()
    qb.pause_multiple(torrents[0][1])


def get_sonarr_history():
    # Instantiate SonarrAPI Object
    sonarr = SonarrAPI(sonarr_host_url, sonarr_api_key)

    # Get and print TV Shows
    hist_list = []
    hist = sonarr.get_history_size(100)
    for record in hist['records']:
        if record['data']['downloadClient'] == 'QBittorrent':
            # print(f"Sonarr: {record['data']['downloadClient']} - {record['sourceTitle']}")
            hist_list.append(record['sourceTitle'])
    return hist_list

if __name__ == '__main__':
    torrents = get_torrents()
    sonarr_list = get_sonarr_history()
    remove_complete_torrents(torrents, sonarr_list)
    pause_complete()
    print("complete")