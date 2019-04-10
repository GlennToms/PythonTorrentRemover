class IParser:

    def __init__(self):
        pass

    def parse_list(self, list):
        pass


class QBitTorrentParser(IParser):

    def __init__(self):
        super.__init__()

    def parse_list(list):
            parsed_list = []
            for torrent in list:
                if torrent['amount_left'] != 0:
                    parsed_list.append((torrent['name'], torrent['hash']))
            return parsed_list


class SonarrParser(IParser):

    def __init__(self):
        super.__init__()

    def parse_list(list):
        hist_list = []
        for record in list['records']:
            if record['data']['downloadClient'] == 'QBittorrent':
                print(f"Sonarr: {record['data']['downloadClient']} - {record['sourceTitle']}")
                hist_list.append(record['sourceTitle'])
        return hist_list


class RadarrParser(IParser):

    def __init__(self):
        super.__init__()

    def parse_list(list):
        hist_list = []
        for record in list['records']:
            if 'downloadClient' in record['data']:
                if record['data']['downloadClient'] == 'QBittorrent':
                    print(f"Radarr: {record['data']['downloadClient']} - {record['sourceTitle']}")
                    hist_list.append(record['sourceTitle'])
        return hist_list
