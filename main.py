# -*- coding: utf-8 -*-

import sched
import time

from Classes import ClientEndpoint, Downloads, Parser

sonarr_client = Downloads.ArrClient(url='http://sonarr.local:6880/api', api_key='589b093bc3484ea5b941173280df0911')
radarr_client = Downloads.ArrClient(url='http://radarr.local:6880/api', api_key='dac2ba0c443f4798b9949a8de76c4d6b')
qbit_client = Downloads.QBitTorrentClient(
    url='http://qbittorrent.local:6880/',
    user='admin',
    password='adminadmin')

s = sched.scheduler(time.time, time.sleep)


def get_downloads(DownloadsClient):
    return DownloadsClient.get()


def completed_torrent_list(download_list, completed_list):
    remove_list = []
    for torrent in download_list:
        for history in completed_list:
            if torrent[0] in history:
                remove_list.append(torrent[1])
    return remove_list


def remove_complete(DownloadsClient, remove_list):
    if len(remove_list) > 0:
        DownloadsClient.remove(remove_list)


def pause_complete(DownloadsClient, pause_list):
    if len(pause_list) > 0:
        DownloadsClient.pause(pause_list)


def parse_list(IParser, torrent_list):
    return IParser.parse_list(torrent_list)


def run():
    torrents = get_downloads(qbit_client)
    download_list = parse_list(Parser.QBitTorrentParser, torrents)

    if len(torrents) > -1:
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


if __name__ == '__main__':
    run()
