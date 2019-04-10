from qbittorrent import Client
from sonarr_api import SonarrAPI


class IDownloadsClient:

    client = None

    def __init__(self, **kwargs):
        pass

    def get(list):
        pass

    def Pause(list):
        pass

    def Stop(list):
        pass

    def Start(self):
        pass


class QBitTorrentClient(IDownloadsClient):

    def __init__(self, **kwargs):
            self.url = kwargs.get('url')
            self.password = kwargs.get('password')
            self.client = Client('http://qbittorrent.local:6880/')
            self.client.login(self.url, self.password)  # not required when 'Bypass from localhost' qb.login()

    def get(self):
        return self.client.torrents()

    def Pause(list):
        pass

    def Stop(list):
        pass

    def Start(self):
        pass


class ArrClient(IDownloadsClient):

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.api_key = kwargs.get('api_key')
        self.client = SonarrAPI(self.url, self.api_key)

    def get(self):
        return self.client.get_history_size(100)

    def Pause(list):
        pass

    def Stop(list):
        pass

    def Start(self):
        pass
