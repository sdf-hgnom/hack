import random
from typing import Text
import time

import requests

N = 10

URLS = ['https://www.avito.ru/',
        'https://www.speedtest.net/',
        'https://djbook.ru/',
        'http://styxcosmetic.ru/',
        'https://www.simplifiedpython.net/',
        'https://ling47.ru/',
        ]


def test_url(what_url: Text, count: int = 10, sleep_time: int = 1) -> float:
    """
    выполнит http get запрос по  адресу если код не 200 сгенирит ошибку
    если все хорошо - подсчитает время выполнения запросов
    :param what_url: url запроса
    :param count: кол-во повторов
    :param sleep_time: задержка между повторами
    :return:
    """
    begin_time = time.monotonic()
    print(f'\nbegin test {what_url} :')
    for i in range(count):
        response = requests.get(url=what_url)
        print('.', end='')
        if response.status_code != 200:
            raise ConnectionError(f'{what_url} -> Bad response code {response.status_code} in {i} iteration ')

        time.sleep(sleep_time)

    return time.monotonic() - begin_time


def get_pass(len: int = 8):
    let = ''.join([chr(i) for i in range(97, 97 + 26)])

    let_up = let.upper()
    simbols = ''.join([chr(i) for i in range(33, 64)])
    alpha = let + let_up + simbols
    new_pass = ''

    for _ in range(len):
        new_pass += random.choice(alpha)
    return new_pass


if __name__ == '__main__':
    for url in URLS:
        try:
            time_period = test_url(what_url=url, count=100, sleep_time=5)
            print(f'\nTest end with {time_period} sec')
        except ConnectionError as ex:
            print(ex.args)
