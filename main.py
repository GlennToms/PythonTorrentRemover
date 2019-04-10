# -*- coding: utf-8 -*-

import sched
import time

import ClientEndpoint
import Downloads
import Parser

sonarr_client = Downloads.ArrClient(url='http://sonarr.local:6880/api', api_key='589b093bc3484ea5b941173280df0911')
radarr_client = Downloads.ArrClient(url='http://radarr.local:6880/api', api_key='dac2ba0c443f4798b9949a8de76c4d6b')
qbit_client = Downloads.QBitTorrentClient(
    url='http://qbittorrent.local:6880/',
    user='admin',
    password='adminadmin')

s = sched.scheduler(time.time, time.sleep)


def get_downloads(DownloadsClient):
    return DownloadsClient.get()


def remove_complete_torrents(torrent_list, sonarr_list):
    remove_list = []
    for torrent in torrent_list:
        for history in sonarr_list:
            if torrent[0] in history:
                print(f"Removing: {torrent[0]}")
                remove_list.append(torrent[1])

    qb.delete_permanently(remove_list)


def pause_complete():
    torrents = get_downloads()
    if len(torrents) > 0:
        qb.pause_multiple(torrents[0][1])


def run():
    torrents = get_downloads(qbit_client)
    download_list = Parser.QBitTorrentParser.parse_list(torrents)

    if len(torrents) > -1:
        sonarr_list = get_downloads(sonarr_client)
        sonarr_list = Parser.SonarrParser.parse_list(sonarr_list)

        radarr_list = get_downloads(radarr_client)
        radarr_list = Parser.RadarrParser.parse_list(radarr_list)

        combined_list = sonarr_list + radarr_list

        remove_complete_torrents(download_list, combined_list)

        pause_complete()
    s.enter(300, 1, run, ())
    s.run()


if __name__ == '__main__':
    run()
