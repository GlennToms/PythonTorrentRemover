# -*- coding: utf-8 -*-

import sched
import time
from qbittorrent import Client
from sonarr_api import SonarrAPI

s = sched.scheduler(time.time, time.sleep)


def run():
    try:
        qb = Client("http://qbittorrent.local:6880")
        qb.login("admin", "adminadmin")
        torrents = qb.torrents(filter="completed")

        downloads = {}
        if len(torrents) > 0:
            for torrent in torrents:
                downloads[torrent["name"]] = torrent["hash"]
                qb.pause(torrent["hash"])

            print(f"Found {len(downloads)} Torrent(s)")

            sonarr_client = SonarrAPI(
                "http://sonarr.local:6880/api", "589b093bc3484ea5b941173280df0911"
            )
            son_hist = sonarr_client.get_history_size(100, 1)
            son_hist2 = sonarr_client.get_history_size(100, 2)

            hist_list = {}
            for record in son_hist["records"]:
                if "eventType" in record:
                    if record["eventType"] == "downloadFolderImported":
                        hist_list[record["sourceTitle"]] = None

            for record in son_hist2["records"]:
                if "eventType" in record:
                    if record["eventType"] == "downloadFolderImported":
                        hist_list[record["sourceTitle"]] = None

            radarr_client = SonarrAPI(
                "http://radarr.local:6880/api", "dac2ba0c443f4798b9949a8de76c4d6b"
            )
            rad_hist = radarr_client.get_history_size(100, 1)
            rad_hist2 = radarr_client.get_history_size(100, 2)

            for record in rad_hist["records"]:
                if "eventType" in record:
                    if record["eventType"] == "downloadFolderImported":
                        hist_list[record["sourceTitle"]] = None

            for record in rad_hist2["records"]:
                if "eventType" in record:
                    if record["eventType"] == "downloadFolderImported":
                        hist_list[record["sourceTitle"]] = None

            lidarr_client = SonarrAPI(
                "http://lidarr.local:6880/api/v1", "3ea81e58ffc149a8803d86c008c8c81e"
            )
            lid_hist = lidarr_client.get_history_size(100)

            lidarr_list = []
            for record in lid_hist["records"]:
                if "eventType" in record:
                    if record["eventType"] == "trackFileImported":
                        # print(f"Removing: {record['sourceTitle']}")
                        lidarr_list.append(record["downloadId"])

            can_remove = []
            for key in downloads.keys():
                for key2 in hist_list.keys():
                    if key2 in key:
                        can_remove.append(key)

            delete_list = []
            for name, hash_ in downloads.items():
                if name in can_remove:
                    print(f'Removing: {name}')
                    delete_list.append(hash_)

            combind_list = list(delete_list) + list(set(lidarr_list))
            qb.delete_permanently(combind_list)

        else:
            print("No torrents in a 'Completed' state.")

    except Exception as e:
        print("FAILED {e}")

    print("Waiting 5 minutes")
    s.enter(300, 1, run, ())
    s.run()


if __name__ == "__main__":
    run()
