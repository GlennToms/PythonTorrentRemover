from qbittorrent import Client
from sonarr_api import SonarrAPI


class IDownloadsClient:

    def __init__(self, **kwargs):
        pass


class QBitTorrentClient(IDownloadsClient):

    def __init__(self, **kwargs):
            self.url = kwargs.get('url')
            self.user = kwargs.get('user')
            self.password = kwargs.get('password')
            self.client = Client(self.url)
            self.client.login(self.user, self.password)  # not required when 'Bypass from localhost' qb.login()
            # self.client.login()

    def get(self):
        a = self.client.torrents()
        return a

    def pause(self, pause_list):
        for item in pause_list:
            self.client.pause_multiple(str(pause_list[1]))

    def stop(list):
        pass

    def start(self):
        pass

    def remove(remove_list):
        # self.client.delete_permanently(remove_list['hash'])
        # print(f'removing {remove_list['hash']}')
        pass


class ArrClient(IDownloadsClient):

    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.api_key = kwargs.get('api_key')
        self.client = SonarrAPI(self.url, self.api_key)

    def get(self):
        return self.client.get_history_size(100)
