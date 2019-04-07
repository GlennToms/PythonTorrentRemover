# -*- coding: utf-8 -*-

from qbittorrent import Client

qb = Client('http://qbittorrent.local:6880/')

#qb.login('admin', 'adminadmin')
qb.login()

# not required when 'Bypass from localhost' setting is active.
# defaults to admin:admin.
# to use defaults, just do qb.login()

def getTorrents():
    torrents = qb.torrents()

    hash_list = []
    for torrent in torrents:
        if torrent['amount_left'] == 0:
            print(f"Removing {torrent['name']}")
            hash_list.append(torrent['hash'])
        else:
            print(f"Not Removing {torrent['name']}")
    return hash_list

def removeTorrent(hash_list):
    qb.delete_permanently(hash_list)


if __name__ == '__main__':
    torrents = getTorrents()
    removeTorrent(torrents)
    