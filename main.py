# -*- coding: utf-8 -*-

from qbittorrent import Client
from sonarr_api import SonarrAPI
import sched, time

qb = Client('http://qbittorrent:8080/')
# qb.login()
qb.login('admin', 'adminadmin') # not required when 'Bypass from localhost' setting is active.


sonarr_host_url = 'http://sonarr:8080/api'
sonarr_api_key = '589b093bc3484ea5b941173280df0911'

radarr_host_url = 'http://radarr:8080/api'
radarr_api_key = 'dac2ba0c443f4798b9949a8de76c4d6b'

s = sched.scheduler(time.time, time.sleep)

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

    qb.delete_permanently(remove_list)


def pause_complete():
    torrents = get_torrents()
    if len(torrents) > 0:
        qb.pause_multiple(torrents[0][1])


def get_sonarr_history():
    # Instantiate SonarrAPI Object
    sonarr = SonarrAPI(sonarr_host_url, sonarr_api_key)

    # Get and print TV Shows
    hist_list = []
    hist = sonarr.get_history_size(100)
    for record in hist['records']:
        if record['data']['downloadClient'] == 'QBittorrent':
            print(f"Sonarr: {record['data']['downloadClient']} - {record['sourceTitle']}")
            hist_list.append(record['sourceTitle'])
    return hist_list


def get_radarr_history():
    # Instantiate SonarrAPI Object
    radarr = SonarrAPI(radarr_host_url, radarr_api_key)

    # Get and print TV Shows
    hist_list = []
    hist = radarr.get_history_size(100)
    for record in hist['records']:
        if 'downloadClient' in record['data']:
            if record['data']['downloadClient'] == 'QBittorrent':
                print(f"Radarr: {record['data']['downloadClient']} - {record['sourceTitle']}")
                hist_list.append(record['sourceTitle'])
    return hist_list


def run():
    torrents = get_torrents()
    if len(torrents) > -1:
        sonarr_list = get_sonarr_history()
        radarr_list = get_radarr_history()
        remove_complete_torrents(torrents, sonarr_list)
        remove_complete_torrents(torrents, radarr_list)
        pause_complete()
    s.enter(300, 1, run, ())
    s.run()


if __name__ == '__main__':
    run()