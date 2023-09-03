import json
from http import HTTPStatus
from urllib.request import urlopen
import datetime
import time
from utils.logger import log


CITIES = {
    "MOSCOW": "https://code.s3.yandex.net/async-module/moscow-response.json",
    "PARIS": "https://code.s3.yandex.net/async-module/paris-response.json",
    "LONDON": "https://code.s3.yandex.net/async-module/london-response.json",
    "BERLIN": "https://code.s3.yandex.net/async-module/berlin-response.json",
    "BEIJING": "https://code.s3.yandex.net/async-module/beijing-response.json",
    "KAZAN": "https://code.s3.yandex.net/async-module/kazan-response.json",
    "SPETERSBURG": "https://code.s3.yandex.net/async-module/spetersburg-response.json",
    "VOLGOGRAD": "https://code.s3.yandex.net/async-module/volgograd-response.json",
    "NOVOSIBIRSK": "https://code.s3.yandex.net/async-module/novosibirsk-response.json",
    "KALININGRAD": "https://code.s3.yandex.net/async-module/kaliningrad-response.json",
    "ABUDHABI": "https://code.s3.yandex.net/async-module/abudhabi-response.json",
    "WARSZAWA": "https://code.s3.yandex.net/async-module/warszawa-response.json",
    "BUCHAREST": "https://code.s3.yandex.net/async-module/bucharest-response.json",
    "ROMA": "https://code.s3.yandex.net/async-module/roma-response.json",
    "CAIRO": "https://code.s3.yandex.net/async-module/cairo-response.json",
    "GIZA": "https://code.s3.yandex.net/async-module/giza-response.json",
    "MADRID": "https://code.s3.yandex.net/async-module/madrid-response.json",
    "TORONTO": "https://code.s3.yandex.net/async-module/toronto-response.json"
}


class UrlStatusException(Exception):
    pass


class RequestErrorException(Exception):
    pass


class YandexWeatherAPI:
    """ Base class for requests """

    def __do_req(url: str) -> str:
        """Base request method"""
        try:
            with urlopen(url) as response:
                resp_body = response.read().decode("utf-8")
                data = json.loads(resp_body)
            if response.status != HTTPStatus.OK:
                raise UrlStatusException(
                    f"Error in {url} request. {resp_body.status}: {resp_body.reason}")
            return data
        except RequestErrorException as ex:
            log.error(ex)
            raise ex(f"Error in {url} request: {ex}")

    def get_forecasting(sel, url):
        return YandexWeatherAPI.__do_req(url)

    def start(self, url):
        while True:
            try:
                res = self.get_forecasting(url)
                with open('weather_inform.txt', 'a+') as text:
                    text.write(f'{datetime.datetime.now().strftime("%d-%m-%Y %H:%M")}: {str(res["info"])}\n')
                log.info('Info has been written')
                break
            except Exception:
                time.sleep(5)
