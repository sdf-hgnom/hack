import random
from typing import Text
import time

import requests

N = 10

urls = ['https://www.speedtest.net/',
        'https://avito.ru/',
        'https://djbook.ru/',
        'http://styxcosmetic.ru/',
        'https://www.simplifiedpython.net/',
        'https://ling47.ru/',
        ]


def test_url(what: Text, count: int = 10):
    begin_time = time.monotonic()
    print(f'\nbegin test {what} :')
    for i in range(count):
        print('.', end='')
        response = requests.get(what)
        if response.status_code != 200:
            raise ConnectionError(f'{what} -> Bad response code {response.status_code} in {i} iteration')
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
    for url in urls:
        try:
            time_period = test_url(what=url, count=10)
            print(f'\nTest end with {time_period} sec')
        except ConnectionError as ex:
            print(ex.args)
