from qbittorrent import Client
from sonarr_api import SonarrAPI


class IDownloadsClient:

    def __init__(self, **kwargs):
        pass

    def get(list):
        pass

    def pause(list):
        pass

    def stop(list):
        pass

    def start(self):
        pass

    def remove(remove_list):
        pass


class QBitTorrentClient(IDownloadsClient):

    def __init__(self, **kwargs):
            self.url = kwargs.get('url')
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.client = Client(self.url)
            self.client.login(self.user, self.password)  # not required when 'Bypass from localhost' qb.login()

    def get(self):
        return self.client.torrents()

    def pause(pause_list):
        self.client.pause_multiple(pause_list)

    def stop(list):
        pass

    def start(self):
        pass

    def remove(remove_list):
        self.client.delete_permanently(remove_list)


class ArrClient(IDownloadsClient):

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.api_key = kwargs.get('api_key')
        self.client = SonarrAPI(self.url, self.api_key)

    def get(self):
        return self.client.get_history_size(100)

    def pause(list):
        pass

    def stop(list):
        pass

    def start(self):
        pass

    def remove(remove_list):
        pass
