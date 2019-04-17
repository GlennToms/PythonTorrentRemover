# -*- coding: utf-8 -*-

import sched
import time
import os
import requests

from Classes import ClientEndpoint, Downloads, Parser

sonarr_client = Downloads.ArrClient(
    url="http://sonarr.local:6880/api", api_key="589b093bc3484ea5b941173280df0911"
)
radarr_client = Downloads.ArrClient(
    url="http://radarr.local:6880/api", api_key="dac2ba0c443f4798b9949a8de76c4d6b"
)
qbit_client = Downloads.QBitTorrentClient(
    url="http://qbittorrent.local:6880/", user="admin", password="adminadmin"
)


# sonarr_client = Downloads.ArrClient(url='http://sonarr:8080/api', api_key='589b093bc3484ea5b941173280df0911')
# radarr_client = Downloads.ArrClient(url='http://radarr:8080/api', api_key='dac2ba0c443f4798b9949a8de76c4d6b')
# qbit_client = Downloads.QBitTorrentClient(
#     url='http://qbittorrent:8080/',
#     user='admin',
#     password='adminadmin')

s = sched.scheduler(time.time, time.sleep)


def get_downloads(IDownloadsClient):
    return IDownloadsClient.get()


def completed_torrent_list(download_list, completed_list):
    remove_list = []
    for torrent in download_list:
        for history in completed_list:
            if torrent[0] in history:
                remove_list.append(torrent[1])
    return remove_list


def remove_complete(IDownloadsClient, remove_list):
    if len(remove_list) > 0:
        IDownloadsClient.remove(remove_list)


def pause_complete(IDownloadsClient, pause_list):
    if len(pause_list) > 0:
        IDownloadsClient.pause(pause_list)


def parse_list(IParser, torrent_list):
    return IParser.parse_list(torrent_list)


def run():
    torrents = get_downloads(qbit_client)

    if len(torrents) > 0:

        download_list = parse_list(Parser.QBitTorrentParser, torrents)
        sonarr_list = get_downloads(sonarr_client)
        sonarr_list = Parser.SonarrParser.parse_list(sonarr_list)

        radarr_list = get_downloads(radarr_client)
        radarr_list = Parser.RadarrParser.parse_list(radarr_list)

        completed_list = sonarr_list + radarr_list
        to_remove_list = completed_torrent_list(download_list, completed_list)

        remove_complete(qbit_client, to_remove_list)

        torrents = get_downloads(qbit_client)
        download_list = parse_list(Parser.QBitTorrentParser, torrents)
        pause_complete(qbit_client, download_list)

    s.enter(300, 1, run, ())
    s.run()


if __name__ == "__main__":
    from qbittorrent import Client
    from sonarr_api import SonarrAPI

    qb = Client('http://qbittorrent.local:6880/')
    qb.login('admin', 'adminadmin')
    torrents = qb.torrents(filter='completed')

    downloads = {}
    if len(torrents) > 0:
        for torrent in torrents:
            downloads[torrent['name']] = torrent['hash']

    sonarr_client = SonarrAPI("http://sonarr.local:6880/api", "589b093bc3484ea5b941173280df0911")
    son_hist = sonarr_client.get_history_size(100)

    hist_list = {}
    for record in son_hist['records']:
        if 'eventType' in record:
            if record['eventType'] == 'downloadFolderImported':
                hist_list[record['sourceTitle']] = None

    radarr_client = SonarrAPI("http://radarr.local:6880/api", "dac2ba0c443f4798b9949a8de76c4d6b")
    rad_hist = radarr_client.get_history_size(100)

    for record in rad_hist['records']:
        if 'eventType' in record:
            if record['eventType'] == 'downloadFolderImported':
                hist_list[record['sourceTitle']] = None

    can_remove = downloads.keys() & hist_list.keys()

    delete_list = []
    for name, hash_ in downloads.items():
        if name in can_remove:
            print(f'IN: {name}')
            delete_list.append(hash_)
        else:
            print(f'OUT: {name}')

    qb.delete_permanently(list(delete_list))
    print("hist_list")
